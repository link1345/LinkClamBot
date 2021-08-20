
import sys

import discord
from discord.ext import tasks

import base.command_base as base
import base.DiscordSend as Sendtool
import command.member_sheet.Config_Main as CSetting

import command.member_sheet.GoogleSheet as CSheet

import gspread
import pandas as pd

import copy

class command(base.command_base)  :

	def __init__(self) :
		super().__init__()

		self.Flag_discord_Member_role = [] # list[]
		self.Flag_discord_Member_id = None
		self.Flag_discord_Member_display_name = None
		self.Flag_discord_Member_name = None
		self.Flag_discord_Member_discriminator = None

		s_index_list = []
		for s_index in CSetting.SheetIndex :
			num = CSetting.SheetIndex.index(s_index) 
			if "text" in s_index.keys() :
				s_index_list.append( s_index["text"]["label"] )
			if "discord.Member.role" in s_index.keys() :
				s_index_list.append( s_index["discord.Member.role"]["name"] )
				self.Flag_discord_Member_role.append( num )
			if "discord.Member.id" in s_index.keys() :
				s_index_list.append( s_index["discord.Member.id"] )
				self.Flag_discord_Member_id = num
			if "discord.Member.display_name" in s_index.keys() :
				s_index_list.append( s_index["discord.Member.display_name"] )
				self.Flag_discord_Member_display_name = num
			if "discord.Member.name" in s_index.keys() :
				s_index_list.append( s_index["discord.Member.name"] )
				self.Flag_discord_Member_name = num
			if "discord.Member.discriminator" in s_index.keys() :
				s_index_list.append( s_index["discord.Member.discriminator"] )
				self.Flag_discord_Member_discriminator = num

		self.CSet_index_list = s_index_list
		print(self.CSet_index_list)
		print( self.Flag_discord_Member_role )
		print( self.Flag_discord_Member_id )
		print( self.Flag_discord_Member_display_name )
		print( self.Flag_discord_Member_name )
		print( self.Flag_discord_Member_discriminator )
		pass


	def getIndex(self, worksheet: gspread.Spreadsheet, member):
		# return は、 「行(member.idが当てはまる行)」 , 「列(col discordID部分)」 

		row_index = worksheet.row_values(1)
		#if not Check_ConfigList( row_index ) :
		if set(row_index) != set(self.CSet_index_list) :
			return None, None

		# ID(列)を取得
		col = worksheet.col_values(self.Flag_discord_Member_id + 1)

		member_point = None
		if str(member.id) in col:
			try :
				member_point = col.index(str(member.id)) + 1
			except IndexError:
				print("名簿にいません")

		row = None
		if member_point is not None :
			row = worksheet.row_values(member_point)
		
		return row, col , member_point

	def changeData(self, old_data:list[str], member:discord.Member) :
		data = copy.deepcopy(old_data)

		# Role
		for item_num in self.Flag_discord_Member_role :
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


		if self.Flag_discord_Member_name is not None :
			data[self.Flag_discord_Member_name] = member.name

		if self.Flag_discord_Member_display_name is not None :
			data[self.Flag_discord_Member_display_name] = member.display_name
		
		return data

	def changeData_User(self, old_data:list[str], member:discord.User) :
		data = copy.deepcopy(old_data)

		# ID
		if self.Flag_discord_Member_id is not None :
			data[self.Flag_discord_Member_id] = str(member.id)
		
		if self.Flag_discord_Member_discriminator is not None :
			data[self.Flag_discord_Member_discriminator] = member.discriminator
		
		if self.Flag_discord_Member_name is not None :
			data[self.Flag_discord_Member_name] = member.name
		
		if self.Flag_discord_Member_display_name is not None :
			data[self.Flag_discord_Member_display_name] = member.display_name

		return data

	async def changeOneData(self, channelID:int, client:discord.Client, before, after, row:list[str], sheetData, member_point=2) :

		change_after = self.changeData(row, after)
		#print("row " , row)
		#print("change_after " , change_after)

		# ロールが全て無くなり名簿から削除する
		flagrole = len(self.Flag_discord_Member_role)
		for item_num in self.Flag_discord_Member_role :
			if change_after[item_num] == "":
				flagrole -= 1
				
		if flagrole == 0 :
			sheetData.delete_row(member_point)
			text="**【自動報告】**" + after.display_name + "さんは、脱退しました"
			await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
			return

		num = 0
		for change_item in change_after :
			# このデータが変更されているか？
			#print(row[num] + " != " +change_item )
			if row[num] != change_item :
				print(row[num] + " != " +change_item )
				# sheet変更
				sheetData.update_cell(member_point, num + 1, change_item)

				# --- 以下、メッセージ文
				# ロール
				for item_num in self.Flag_discord_Member_role :
					if num == item_num :
						text="**【自動報告】**" + after.display_name + "さんの、役職が変更されました"
						if row[num] == "〇" :
							text = "**【自動報告】**" + after.display_name + "さんは、" + CSetting.SheetIndex[item_num]["discord.Member.role"]["name"] + "が剥奪されました"				
						else :
							text = "**【自動報告】**" + after.display_name + "さんは、" + CSetting.SheetIndex[item_num]["discord.Member.role"]["name"] + "を付与されました"
						await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)

				# ID
				if self.Flag_discord_Member_id is not None and self.Flag_discord_Member_id == num :
					text = "**【自動報告】**" + after.display_name + "さんのIDが変更されました。"
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)

				#
				if self.Flag_discord_Member_display_name is not None and self.Flag_discord_Member_display_name == num :
					text = "**【自動報告】**" + before.display_name + "さんのニックネームが、**"+ after.display_name +"**に変わりました。"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member_name is not None and self.Flag_discord_Member_name == num:
					text = "**【自動報告】**" + before.display_name + "(" + before.name +")さんのシステム名前が、" + after.name + "に変更されました"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member_discriminator is not None and self.Flag_discord_Member_discriminator == num:
					# discriminator は…メッセージ要らんでしょ。
					pass

			num += 1
		pass


	async def changeOneData_User(self, channelID:int, client:discord.Client, before, after, row:list[str], sheetData, member_point=2) :

		change_after = self.changeData_User(row, after)
		print("row " , row)
		print("change_after " , change_after)

		# ロールが全て無くなり名簿から削除する
		num = 0
		for change_item in change_after :
			# このデータが変更されているか？
			#print(row[num] + " != " +change_item )
			if row[num] != change_item :
				print(row[num] + " != " +change_item )
				# sheet変更
				sheetData.update_cell(member_point, num + 1, change_item)

				# --- 以下、メッセージ文
				# ID
				if self.Flag_discord_Member_id is not None and self.Flag_discord_Member_id == num :
					text = "**【自動報告】**" + after.display_name + "さんのIDが変更されました。"
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)

				#
				if self.Flag_discord_Member_display_name is not None and self.Flag_discord_Member_display_name == num :
					text = "**【自動報告】**" + before.display_name + "さんのニックネームが、**"+ after.display_name +"**に変わりました。"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member_name is not None and self.Flag_discord_Member_name == num:
					text = "**【自動報告】**" + before.display_name + "(" + before.name +")さんのシステム名前が、" + after.name + "に変更されました"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member_discriminator is not None and self.Flag_discord_Member_discriminator == num:
					# discriminator は…メッセージ要らんでしょ。
					pass

			num += 1
		pass



	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		await Sendtool.Send_Member(Data=message, message="auto test message", filename=None)

	
	async def on_member_update(self, config, client: discord.Client, before: discord.Member, after: discord.Member) :

		changeFlag = False

		if before.display_name != after.display_name :
			changeFlag = True

		if before.name != after.name or before.discriminator != after.discriminator :
			changeFlag = True

		def makelist_roleID(member: discord.Member ):
			ID = []
			print(member.roles)
			for role in member.roles :
				ID.append( role.id )
			return ID


		before_roleID = makelist_roleID( before )
		after_roleID = makelist_roleID( after )
		if set(before_roleID) != set(after_roleID) : 
			addItem =  list( set(after_roleID) - set(before_roleID) )
			deleteItem =  list( set(before_roleID) - set(after_roleID) )
			print("delete : " , deleteItem)
			print("add : " , addItem)
			changeFlag = True

		if changeFlag :
			sheetData = CSheet.getGooglesheet()
			if sheetData is None :
				return
			row = []
			col = []
			member_point = None
			row, col, member_point = self.getIndex(sheetData, before)
			print("row : " , row)
			print("col : " , col)
			print(" member_point : " , member_point)

			if row is None and col is None :
				# 名簿がおかしい				
				text = "**【ERROR】**Botで設定されているindexとGoogleSheetのindexが違います。修正お願い致します。"
				await Sendtool.Send_ChannelID(client=client, channelID=CSetting.AutoEvent_ERRORMessage_channelID, message=text, filename=None)
				return 

			if member_point is None or row is None or row == [] :
				# 名簿に存在しないので、新規登録
				print("user Add")
				row = [""] * len(self.CSet_index_list)
				row = self.changeData(row, after)
				print("user Add ROW : " , row)
				sheetData.append_row(row)
				print("user Add OK")
				return 
			
			# ただの変更の場合。
			## 変更があったところだけ更新して終わり。
			await self.changeOneData(channelID=CSetting.AutoEvent_ERRORMessage_channelID, client=client, before=before, after=after, row=row,  sheetData=sheetData, member_point=member_point)
			print("user changeOneData OK")

		pass


	async def on_member_remove( self, config, client: discord.Client, member: discord.Member ) :
		sheetData = CSheet.getGooglesheet()
		if sheetData is None :
			return
		row, col, member_point = self.getIndex(sheetData, member)

		if member_point is not None :
			sheetData.delete_row(member_point)
			text="**【自動報告】**" + member.display_name + "さんは、脱退しました"
			await Sendtool.Send_ChannelID(client=client, channelID=CSetting.AutoEvent_ERRORMessage_channelID, message=text, filename=None)

		pass

	async def on_user_update( self, config, client: discord.Client, before: discord.User, after: discord.User ) :
		print("test user update")


		sheetData = CSheet.getGooglesheet()
		row, col, member_point = self.getIndex(sheetData, before)
		print("row : " , row)
		print("col : " , col)
		print(" member_point : " , member_point)

		await self.changeOneData_User(channelID=CSetting.AutoEvent_ERRORMessage_channelID, client=client, before=before, after=after, row=row, sheetData=sheetData, member_point=member_point)

		pass

	async def on_member_join( self, config, client: discord.Client, member: discord.Member ) :
		#print("test member join")
		pass