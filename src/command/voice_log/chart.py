import discord
import os
import json

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from pprint import pprint

import base.ColorPrint as CPrint

import command.voice_log.Config_Main as CSetting

def most_old_Month() :

	old_month =	1
	labels = []
	fileNameList = []
	while True :
		filetime = datetime.datetime.today() - relativedelta(months=old_month)
		m_month = datetime.datetime.strftime(filetime,'%m')
		m_year = datetime.datetime.strftime(filetime,'%Y')
		filename = CSetting.baseLogFolder + CSetting.JSONPATH_row + m_year + m_month + ".json"
		if not os.path.exists( filename ) :
			old_month -= 1 # 調査用に+1してあるので、実際の値は、これにold_monthに-1したものとなる。
			break
		
		labels.append( m_year + "/" + m_month )
		fileNameList.append( filename )

		old_month += 1

	return old_month , labels , fileNameList

async def makeOldTimeList( client: discord.Client, MonthFileList:list[str] , IndexLabel:list[str], RoleList: list[int] = CSetting.OneMonthOutput_RoleID ):
	all_df = None
	for fileName in MonthFileList :
		df = await makeTimeList( client, Datafile_path=fileName , RoleList=RoleList)
		
		#print( "test1" )
		pprint( df )
		if df is None :
			break

		labelname = IndexLabel[MonthFileList.index(fileName)]
		df = df.rename(columns={'time': labelname })

		if MonthFileList.index(fileName) == 0 :
			all_df = df
		else :
			df = df.drop(columns=['name'])
			all_df = pd.merge(all_df, df , left_index=True, right_index=True)
			#all_df = pd.merge(all_df, df , left_index=True)
			#df.loc[:,[labelname]]

	#pprint(all_df)
	return all_df

async def UserRoleMember( client: discord.Client, RoleList: list[int] ) :
	"""
	[VC] 指定ロールに参加しているメンバーを抽出する
 
	Args:
		client (discord.Client): クライアント
		RoleList (list[int]): 役職ID
	return:
		list[discord.Member]: 指定ロールに参加しているメンバー
	"""

	data = []
	for guild_item in client.guilds :

		# ギルドデータ更新
		await guild_item.chunk()

		# ロール制限がなければ、全員分を取ってくる
		if len(RoleList) == 0 :
			data += guild_item.members
			continue

		# ロール制限がなければ、該当ロール部を取ってくる
		for role_item in guild_item.roles :
			if role_item.id in RoleList :
				data += role_item.members
	
	return data


async def makeTimeList( client: discord.Client, Datafile_path: str , RoleList: list[int]):
	"""
	[VC] 生のログデータを計算して、表にして返す。
 
	Args:
		client (discord.Client): クライアント
		RoleList (list[int]): 役職ID
		mode (string): ユーザーを示すものは、何か？(UserName or ID)
	return:
		pd.DataFrame: 計算済みデータ
	"""
	# ユーザーリスト取得
	members = await UserRoleMember(client, RoleList)

	# IDだけ抽出
	def getID(members: list[discord.Member]):
		IDlist = []
		Namelist = []
		for member in members :
			IDlist.append( member.id )
			Namelist.append( member.name + "#" + member.discriminator )
		return IDlist , Namelist

	members_IDlist , members_Namelist = getID(members=members)
	
	if members_IDlist is None or members_IDlist == [] :
		return None

	# JSON取得
	orig_TimeData : dict
	try :
		with open( Datafile_path ) as f:
			orig_TimeData = json.load(f)
	except :
		CPrint.error_print("JSONではありません")
		import traceback
		traceback.print_exc()
		return None
	
	if orig_TimeData is None :
		return None

	#df = pd.DataFrame({
	#	'start': [None, None],
	#	'end': [None, None],
	#	'time': [13, 23]},
	#	index=['ONE', 'TWO']
	#)

	df_dict = {
		'name': members_Namelist,
		'start': [None] * len(members),
		'exit': [None] * len(members),
		'time': [0.0] * len(members),
	}

	# 計算
	for item in orig_TimeData :
		try :
			indexNum = members_IDlist.index(item["member.id"])
		except ValueError as error :
			# 現在の鯖に、存在しない人は処理しない。
			continue

		if item["Flag"] == "entry" :
			 df_dict["start"][indexNum] = item["time"]
		if item["Flag"] == "exit" :
			# スタートがないのに、エンドがある場合
			if df_dict["start"][indexNum] is None :
				# とりあえず、月初めに入室した扱いにする(他の方法も検討中。そもそも入室してない扱いetc..)
				tmp_startTime = datetime.now().strftime("%Y/%m/01 00:00:00")
				df_dict["start"][indexNum] = tmp_startTime

			# --
			df_dict["exit"][indexNum] = item["time"]

			# 差分計算
			a_time = datetime.datetime.strptime( df_dict["start"][indexNum] , '%Y/%m/%d %H:%M:%S')
			b_time = datetime.datetime.strptime( df_dict["exit"][indexNum] , '%Y/%m/%d %H:%M:%S')


			time : float = (b_time - a_time).total_seconds()
			#print( "time : " + str(time) )
			if time < 0.0 :
				df_dict["time"][indexNum] += 0.0
			else :
				df_dict["time"][indexNum] += time

	# DataFrameに変更
	df = pd.DataFrame(df_dict,
		index=members_IDlist
	)

	# 作業用の"start"と"end"を削除
	df = df.drop(columns=['start','exit'])

	# 計算
	df["time"] = df["time"] / 60 / 60

	#pprint(df)

	return df

