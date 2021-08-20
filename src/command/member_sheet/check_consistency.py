
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

	def changeData(self, old_data:list[str], member:discord.Member) :
		data = copy.deepcopy(old_data)

		# Role
		for item_num in self.Flag_discord_Member["role"] :
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

		if self.Flag_discord_Member["id"] is not None :
			data[self.Flag_discord_Member["id"]] = str(member.id)
			
		if self.Flag_discord_Member["discriminator"] is not None :
			data[self.Flag_discord_Member["discriminator"]] = member.discriminator

		if self.Flag_discord_Member["name"] is not None :
			data[self.Flag_discord_Member["name"]] = member.name

		if self.Flag_discord_Member["display_name"] is not None :
			data[self.Flag_discord_Member["display_name"]] = member.display_name
		
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
		print(indexName)
		print(sheetIndexNumber)
		worksheet = CSheet.getGooglesheet()
		sheet_col , sheet_displayName_col = CSheet.getIndex_AllMember(worksheet, indexName, sheetIndexNumber)

		if sheet_col is None or sheet_displayName_col is None :
			await Sendtool.Send_Member(Data=message, message="表壊れてる")
		
		# 名簿に存在するか？
		#print(sheet_col)
		#print(sheet_displayName_col)
		del_uesrs = list(set(sheet_col) - set(userList_id)) # sheetに過剰に存在する
		add_users = list(set(userList_id) - set(sheet_col)) # sheetに存在しない

		# 要らないデータ削除
		for user in del_uesrs :
			worksheet.delete_row( sheet_col.index(user) + 1 )
			time.sleep(0.3)

		# 再度データ撮り直し。
		worksheet = CSheet.getGooglesheet()
		sheet_col , sheet_displayName_col = CSheet.getIndex_AllMember(worksheet, indexName, sheetIndexNumber)

		if sheet_col is None or sheet_displayName_col is None :
			await Sendtool.Send_Member(Data=message, message="表壊れてる")

		# 現在いるユーザー更新
		for num in range( len(sheet_col) ) :
			old_user_row = worksheet.row_values( num + 1 ) 
			#print( "old_user_row : ", old_user_row )
			print( "member : " , userList[ userList_id.index( sheet_col[num] ) ] )
			new_user_row = self.changeData(old_user_row,  userList[ userList_id.index( sheet_col[num] ) ] )

			print(old_user_row)
			print(new_user_row)

			check_index_num = 0
			for change_item in change_after :
				if old_user_row[check_index_num] != change_item :			
					print( "hit : ", old_user_row , " != " , change_item )
					sheetData.update_cell( num + 1 , check_index_num , change_item)
					time.sleep(0.3)
				check_index_num += 1
			
		# 新しいデータ追加
		for user in add_users :
			new_user_row = [""] * len(indexName)
			print( "member : " , userList[ userList_id.index( sheet_col[num] ) ] )
			new_user_row = self.changeData(new_user_row,  userList[ userList_id.index( sheet_col[num] ) ] )
			worksheet.append_row( new_user_row )

		pass



		############### ＼(^o^)／　つかれた。明日の私頑張れ