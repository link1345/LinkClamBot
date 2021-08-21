
import sys

import discord
from discord.ext import tasks

import base.command_base as base
import base.DiscordSend as Sendtool
import command.member_sheet.Config_Main as CSetting
import command.member_sheet.GoogleSheet as CSheet

import pandas as pd

from discord.ext import tasks

import copy
import time

class command(base.command_base)  :

	def __init__(self) :
		super().__init__()

		pass

	def changeData(self, old_data:list[str], member:discord.Member, sheetIndexNumber) :
		data = copy.deepcopy(old_data)

		# Role
		for item_num in sheetIndexNumber["role"] :
			#print( "role test " ,  CSetting.SheetIndex[item_num] )
			item = CSetting.SheetIndex[item_num]["discord.Member.role"]
			Flag_role_hit = False
			
			member_roles = []
			for mRole in member.roles :
				member_roles.append( mRole.id )

			diffeRole = list( set(member_roles) - set(item["roles"]) ) 
			if  len(member_roles) != len(diffeRole) :
				data[item_num] = "〇"
			else :
				data[item_num] = ""

		if sheetIndexNumber["id"] is not None :
			data[sheetIndexNumber["id"]] = str(member.id)
			
		if sheetIndexNumber["discriminator"] is not None :
			data[sheetIndexNumber["discriminator"]] = member.discriminator

		if sheetIndexNumber["name"] is not None :
			data[sheetIndexNumber["name"]] = member.name

		if sheetIndexNumber["display_name"] is not None :
			data[sheetIndexNumber["display_name"]] = member.display_name
		
		return data

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		#await Sendtool.Send_Member(Data=message, message="interactive test message", filename=None)

		sheetIndexNumber, indexName = CSheet.SettingIndex()

		# 名簿に入るロール一覧を作る
		set_roles = [] 
		for num in sheetIndexNumber["role"] :
			set_roles += CSetting.SheetIndex[num]["discord.Member.role"]["roles"]


		userList = []
		for guildItem in client.guilds :
			
			# そもそもこの鯖に名簿に記載する条件のロールは存在するか？
			guild_flag = False
			for guild_roles in guildItem.roles :
				if guild_roles.id in set_roles :
					guild_flag = True
					break
			
			if not guild_flag :
				continue

			# メンバーがロールを持っているか？	
			for member in guildItem.members :
				for member_role in member.roles :
					if member_role.id in set_roles :
						userList.append( member )
		
		# リストを重複なしに
		userList = list(set(userList))
		
		userList_id = []
		for user in userList : 
			userList_id.append( str(user.id) )
		
		# 名簿取得
		#print(indexName)
		#print(sheetIndexNumber)
		worksheet = CSheet.getGooglesheet()
		sheet_col , sheet_displayName_col = CSheet.getIndex_AllMember(worksheet, indexName, sheetIndexNumber)

		if sheet_col is None or sheet_displayName_col is None :
			await Sendtool.Send_Member(Data=message, message="【ERROR】名簿の形式が壊れていませんか？")
		
		# 名簿に存在するか？
		#print(sheet_col)
		#print(sheet_displayName_col)
		del_uesrs = list(set(sheet_col) - set(userList_id)) # sheetに過剰に存在する
		add_users = list(set(userList_id) - set(sheet_col)) # sheetに存在しない

		#print("del_uesrs " , del_uesrs)
		#print("add_users " , add_users )
		
		# 要らないデータ削除		
		await Sendtool.Send_Member(Data=message, message="【報告】要らないデータを削除しています...")
		for user in del_uesrs :
			await Sendtool.Send_Member(Data=message, message="")
			worksheet.delete_row( sheet_col.index(user) + 1 )
			time.sleep(0.3)

		# 再度データ撮り直し。
		worksheet = CSheet.getGooglesheet()
		sheet_col , sheet_displayName_col = CSheet.getIndex_AllMember(worksheet, indexName, sheetIndexNumber)

		#print("sheet_col " , sheet_col)
		#print("sheet_displayName_col " , sheet_displayName_col )

		if sheet_col is None or sheet_displayName_col is None :
			await Sendtool.Send_Member(Data=message, message="【ERROR】名簿の形式が壊れていませんか？")

		# 現在いるユーザー更新
		await Sendtool.Send_Member(Data=message, message="【報告】欠損しているデータを埋めています...")
		for num in range( len(sheet_col) ) :
			old_user_row = worksheet.row_values( num + 2 ) 

			if len(indexName) - len(old_user_row) > 0 :
				old_user_row += [""] * ( len(indexName) - len(old_user_row) )

			#print( "old_user_row : ", old_user_row )
			#print( "member : " , userList[ userList_id.index( sheet_col[num] ) ] )
			change_after  = self.changeData(old_user_row,  userList[ userList_id.index( sheet_col[num] ) ] , sheetIndexNumber )

			#print("change_after  " , change_after )

			check_index_num = 0
			for change_item in change_after :
				if old_user_row[check_index_num] != change_item :			
					#print( "hit : ", old_user_row[check_index_num] , " != " , change_item )
					worksheet.update_cell( num + 2 , check_index_num + 1 , change_item)
					time.sleep(0.3)
				check_index_num += 1
			
		# 新しいデータ追加
		await Sendtool.Send_Member(Data=message, message="【報告】名簿にないユーザーを追加しています...")
		for user in add_users :
			change_after  = [""] * len(indexName)
			#print( "member : " , userList[ userList_id.index( user ) ] )
			change_after  = self.changeData(change_after ,  userList[ userList_id.index( user ) ] , sheetIndexNumber )
			worksheet.append_row( change_after  )


		await Sendtool.Send_Member(Data=message, message="**【終了】名簿の整合性チェックが終わりました。**")
		await Sendtool.Send_Member(Data=message, message="【名簿URL】" + CSetting.SPREADSHEET_URL , filename=None)

		pass



		############### ＼(^o^)／　つかれた。明日の私頑張れ