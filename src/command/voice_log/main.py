
import sys

import discord
from discord.ext import tasks

import base.command_base as base

import base.DiscordSend as Sendtool
import base.ColorPrint as CPrint
import base.time_check as CTime

import os
import collections as cl
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

import command.voice_log.Config_Main as CSetting
import command.voice_log.chart as Chart


import pandas as pd

class command(base.command_base)  :

	def __init__(self) :
		super().__init__()
		self.test_task: tasks.Loop = None

		self.now_filepath = CSetting.baseLogFolder + CSetting.JSONPATH_row + CSetting.JSONPATH_now

	# JSON記入
	## https://qiita.com/KEINOS/items/ea4bda15506bbd3e6913 から勝手に拝借
	def append_json_to_file(self, _dict, path_file):
		try :
			with open(path_file, 'ab+') as f:              # ファイルを開く
				f.seek(0,2)                                # ファイルの末尾（2）に移動（フォフセット0）  
				if f.tell() == 0 :                         # ファイルが空かチェック
					f.write(json.dumps([_dict],indent=4,ensure_ascii=False).encode())  # 空の場合は JSON 配列を書き込む
				else :
					f.seek(-1,2)                           # ファイルの末尾（2）から -1 文字移動
					f.truncate()                           # 最後の文字を削除し、JSON 配列を開ける（]の削除）
					f.write(' , '.encode())                # 配列のセパレーターを書き込む
					f.write(json.dumps(_dict,indent=4,ensure_ascii=False).encode())    # 辞書を JSON 形式でダンプ書き込み
					f.write(']'.encode())                  # JSON 配列を閉じる
		
		except OSError as e:
			CPrint.error_print( path_file + "が、存在しませんでした")
			print(os.getcwd())
			print(e)

		return f.close() # 連続で追加する場合は都度 Open, Close しない方がいいかも

	# JSON出力(1ヵ月定期・ファイルチェンジ機能付き)
	async def MonthOutput(self, client: discord.Client):
		today = datetime.today()
		filetime = today - relativedelta(months=1)
 
		# Renameするときのファイル名を決定する
		m_month = datetime.strftime(filetime,'%m')
		m_year = datetime.strftime(filetime,'%Y')
		month_filename = '{0}{1}'.format(m_year, m_month)
		mv_filename = CSetting.baseLogFolder + CSetting.JSONPATH_row + month_filename + ".json"

		if os.path.exists(self.now_filepath) == False:
			# ここにエラー文を出して置く
			return None

		# Rename
		os.rename(self.now_filepath, mv_filename )

		# now生ログファイルを、空作成しておく
		with open( self.now_filepath ,"w"):pass
	
		# 加工済みデータを作る
		timeData = await Chart.makeTimeList(client, mv_filename , CSetting.OneMonthOutput_RoleID , mode="NAME")

		# CSVで加工済みを保存する
		if timeData is not None :
			send_fileName = CSetting.baseLogFolder + CSetting.JSONPATH_analysis + month_filename + ".csv"
			timeData.to_csv( send_fileName )
			return send_fileName
		else :
			return None


	#async def on_message(self, config, client: discord.Client, message: discord.Message) :
		#sendfile = await self.MonthOutput(client=client)
		#if sendfile is None :
		#	await Sendtool.Send_Member(Data=message, message="ログファイルがありませんでした。", filename=None)
		#else :
		#	await Sendtool.Send_Member(Data=message, message="MonthOutput!", filename=sendfile)
		#pass


	## 入退室監視
	async def on_voice_state_update(self, config, client: discord.Client, member: discord.Member, before: discord.VoiceState , after: discord.VoiceState):
		data = cl.OrderedDict()

		if before.channel is None:
			## 入ってきたら
			print( datetime.now().strftime("%Y/%m/%d %H:%M:%S") ,":" , after.channel.name, "から" , member.name , "#" , member.discriminator , "さんが入りました")
			data["Flag"] = "entry"
			data["before.channel.name"] = "NULL"
			data["before.channel.id"] = "NULL"
			data["after.channel.name"] = after.channel.name
			data["after.channel.id"] = after.channel.id
			data["member.name"] = member.name
			data["member.discriminator"] = member.discriminator
			data["member.id"] = member.id
			data["time"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
 
		elif after.channel is None:
			## 抜けたら 
			print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") ,":" , before.channel.name, "から" , member.name , "#" , member.discriminator , "さんが抜けました")
			data["Flag"] = "exit"
			data["before.channel.name"] = before.channel.name
			data["before.channel.id"] = before.channel.id
			data["after.channel.name"] = "NULL"
			data["after.channel.id"] = "NULL"
			data["member.name"] = member.name
			data["member.discriminator"] = member.discriminator
			data["member.id"] = member.id
			data["time"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

		elif after.channel.id != before.channel.id :
			print(datetime.now().strftime("%Y/%m/%d %H:%M:%S") ,":" , before.channel.name, "から" , member.name , "#" , member.discriminator , "さんが移動しました")
			data["Flag"] = "move"
			data["before.channel.name"] = before.channel.name
			data["before.channel.id"] = before.channel.id
			data["after.channel.name"] = after.channel.name
			data["after.channel.id"] = after.channel.id
			data["member.name"] = member.name
			data["member.discriminator"] = member.discriminator
			data["member.id"] = member.id
			data["time"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		else :
			# 特になし
			pass

		self.append_json_to_file( data, self.now_filepath )

		pass


	# 定期送信(1ヵ月)
	async def voice_outputlog(self, config, client: discord.Client):
		
		channellist = []
		if config.get("on_task") is not None :
			if config["on_task"].get(sys._getframe().f_code.co_name) is not None :
				channellist = config["on_task"][sys._getframe().f_code.co_name].get("message-channelID")
				
		if channellist is None :
			return 

		#await Sendtool.Send_ChannelID(client=client, channelID=channellist , message="TASKCheck! - voice_outputlog")


		## --------

		flag = False

		# 動作時間決定
		# ※ 指定日時に動作できないので、これで代用。
		TestFlag = False # --- 定期実行のプログラムテスト以外では、これは、Falseにしてください --------------
		if TestFlag == False : # 1日に実行する
			flag =  CTime.check('%d %H', '01 00')
		else :                 # 1時に実行する
			flag =  CTime.check('%M', '00')

		
		# -- 出力処理 --	
		if flag :
			sendfile = await self.MonthOutput(client=client)

			filetime = today - relativedelta(months=1)
			m_month = datetime.strftime(filetime,'%m')
			m_year = datetime.strftime(filetime,'%Y')
			month_filename = '{0}{1}'.format(m_year, m_month)
			mv_filename = CSetting.baseLogFolder + CSetting.JSONPATH_row + month_filename + ".json"
				
			if sendfile is None :
				text = "【一か月定期連絡】"+ m_year + "年"+ m_month +"月の音声チャンネルログインはありませんでした"
				await Sendtool.Send_ChannelID(client=client, channelID=CSetting.OneMonthOutput_ChannelID, message=text, filename=None)
			else :
				text = "【一か月定期連絡】"+ m_year + "年"+ m_month +"月の音声チャンネルログイン生データ"
				await Sendtool.Send_ChannelID(client=client, channelID=CSetting.OneMonthOutput_ChannelID, message=text, filename=mv_filename)
				text = "【一か月定期連絡】"+ m_year + "年"+ m_month +"月の音声チャンネルログイン加工データ"
				await Sendtool.Send_ChannelID(client=client, channelID=CSetting.OneMonthOutput_ChannelID, message=text, filename=sendfile)
			pass

		pass