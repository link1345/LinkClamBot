
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

		self.Flag_discord_Member, self.CSet_index_list = CSheet.SettingIndex()
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


		if self.Flag_discord_Member["name"] is not None :
			data[self.Flag_discord_Member["name"]] = member.name

		if self.Flag_discord_Member["display_name"] is not None :
			data[self.Flag_discord_Member["display_name"]] = member.display_name
		
		return data


	def changeData_User(self, old_data:list[str], member:discord.User) :
		data = copy.deepcopy(old_data)

		# ID
		if self.Flag_discord_Member["id"] is not None :
			data[self.Flag_discord_Member["id"]] = str(member.id)
		
		if self.Flag_discord_Member["discriminator"] is not None :
			data[self.Flag_discord_Member["discriminator"]] = member.discriminator
		
		if self.Flag_discord_Member["name"] is not None :
			data[self.Flag_discord_Member["name"]] = member.name
		
		if self.Flag_discord_Member["display_name"] is not None :
			data[self.Flag_discord_Member["display_name"]] = member.display_name

		return data


	async def changeOneData(self, channelID:int, client:discord.Client, before, after, row:list[str], sheetData, member_point=2) :

		change_after = self.changeData(row, after)
		#print("row " , row)
		#print("change_after " , change_after)

		# ロールが全て無くなり名簿から削除する
		flagrole = len(self.Flag_discord_Member["role"])
		for item_num in self.Flag_discord_Member["role"] :
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
				#print(row[num] + " != " +change_item )
				# sheet変更
				sheetData.update_cell(member_point, num + 1, change_item)

				# --- 以下、メッセージ文
				# ロール
				for item_num in self.Flag_discord_Member["role"] :
					if num == item_num :
						text="**【自動報告】**" + Sendtool.text_check(after.display_name) + "さんの、役職が変更されました"
						if row[num] == "〇" :
							text = "**【自動報告】**" + Sendtool.text_check(after.display_name) + "さんは、" + Sendtool.text_check(CSetting.SheetIndex[item_num]["discord.Member.role"]["name"]) + "が剥奪されました"				
						else :
							text = "**【自動報告】**" + Sendtool.text_check(after.display_name) + "さんは、" + Sendtool.text_check(CSetting.SheetIndex[item_num]["discord.Member.role"]["name"]) + "を付与されました"
						await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)

				# ID
				if self.Flag_discord_Member["id"] is not None and self.Flag_discord_Member["id"] == num :
					text = "**【自動報告】**" + Sendtool.text_check(after.display_name) + "さんのIDが変更されました。"
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)

				#
				if self.Flag_discord_Member["display_name"] is not None and self.Flag_discord_Member["display_name"] == num :
					text = "**【自動報告】**" + Sendtool.text_check(before.display_name) + "さんのニックネームが、**"+ Sendtool.text_check(after.display_name) +"**に変わりました。"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member["name"] is not None and self.Flag_discord_Member["name"] == num:
					text = "**【自動報告】**" + Sendtool.text_check(before.display_name) + "(" + Sendtool.text_check(before.name) +")さんのシステム名前が、" + Sendtool.text_check(after.name) + "に変更されました"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member["discriminator"] is not None and self.Flag_discord_Member["discriminator"] == num:
					# discriminator は…メッセージ要らんでしょ。
					pass

			num += 1
		pass


	async def changeOneData_User(self, channelID:int, client:discord.Client, before, after, row:list[str], sheetData, member_point=2) :

		change_after = self.changeData_User(row, after)
		#print("row " , row)
		#print("change_after " , change_after)

		# ロールが全て無くなり名簿から削除する
		num = 0
		for change_item in change_after :
			# このデータが変更されているか？
			#print(row[num] + " != " +change_item )
			if row[num] != change_item :
				#print(row[num] + " != " +change_item )
				# sheet変更
				sheetData.update_cell(member_point, num + 1, change_item)

				# --- 以下、メッセージ文
				# ID
				if self.Flag_discord_Member["id"] is not None and self.Flag_discord_Member["id"] == num :
					text = "**【自動報告】**" + Sendtool.text_check(after.display_name) + "さんのIDが変更されました。"
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)

				# name
				if self.Flag_discord_Member["name"] is not None and self.Flag_discord_Member["name"] == num:
					text = "**【自動報告】**" + Sendtool.text_check(before.display_name) + "(" + Sendtool.text_check(before.name) +")さんのシステム名前が、" + Sendtool.text_check(after.name) + "に変更されました"					
					await Sendtool.Send_ChannelID(client=client, channelID=channelID, message=text, filename=None)
				
				if self.Flag_discord_Member["discriminator"] is not None and self.Flag_discord_Member["discriminator"] == num:
					# discriminator は…メッセージ要らんでしょ。
					pass

			num += 1
		pass



	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		#await Sendtool.Send_Member(Data=message, message="auto test message", filename=None)
		pass
	
	async def on_member_update(self, config, client: discord.Client, before: discord.Member, after: discord.Member) :

		changeFlag = False

		if before.display_name != after.display_name :
			changeFlag = True

		if before.name != after.name or before.discriminator != after.discriminator :
			changeFlag = True

		def makelist_roleID(member: discord.Member ):
			ID = []
			#print(member.roles)
			for role in member.roles :
				ID.append( role.id )
			return ID


		before_roleID = makelist_roleID( before )
		after_roleID = makelist_roleID( after )
		if set(before_roleID) != set(after_roleID) : 
			addItem =  list( set(after_roleID) - set(before_roleID) )
			deleteItem =  list( set(before_roleID) - set(after_roleID) )
			#print("delete : " , deleteItem)
			#print("add : " , addItem)
			changeFlag = True

		if changeFlag :
			sheetData = CSheet.getGooglesheet()
			if sheetData is None :
				return
			row = []
			col = []
			member_point = None
			row, col, member_point = CSheet.getIndex(sheetData, before, self.CSet_index_list, self.Flag_discord_Member)
			#print("row : " , row)
			#print("col : " , col)
			#print(" member_point : " , member_point)

			if row is None and col is None :
				# 名簿がおかしい				
				text = "**【ERROR】**Botで設定されているindexとGoogleSheetのindexが違います。修正お願い致します。"
				await Sendtool.Send_ChannelID(client=client, channelID=CSetting.AutoEvent_ERRORMessage_channelID, message=text, filename=None)
				return 

			if member_point is None or row is None or row == [] :
				# 名簿に存在しないので、新規登録
				#print("user Add")
				row = [""] * len(self.CSet_index_list)
				row = self.changeData(row, after)
				#print("user Add ROW : " , row)
				sheetData.append_row(row)
				#print("user Add OK")
				return 
			
			# ただの変更の場合。
			## 変更があったところだけ更新して終わり。
			await self.changeOneData(channelID=CSetting.AutoEvent_ERRORMessage_channelID, client=client, before=before, after=after, row=row,  sheetData=sheetData, member_point=member_point)
			#print("user changeOneData OK")

		pass


	async def on_member_remove( self, config, client: discord.Client, member: discord.Member ) :
		sheetData = CSheet.getGooglesheet()
		if sheetData is None :
			return
		row, col, member_point = CSheet.getIndex(sheetData, member, self.CSet_index_list, self.Flag_discord_Member)

		if member_point is not None :
			sheetData.delete_row(member_point)
			text="**【自動報告】**" + Sendtool.text_check(member.display_name) + "さんは、脱退しました"
			await Sendtool.Send_ChannelID(client=client, channelID=CSetting.AutoEvent_ERRORMessage_channelID, message=text, filename=None)

		pass


	async def on_user_update( self, config, client: discord.Client, before: discord.User, after: discord.User ) :
		#print("test user update")

		sheetData = CSheet.getGooglesheet()
		row, col, member_point = CSheet.getIndex(sheetData, before, self.CSet_index_list, self.Flag_discord_Member)
		#print("row : " , row)
		#print("col : " , col)
		#print(" member_point : " , member_point)
		
		await self.changeOneData_User(channelID=CSetting.AutoEvent_ERRORMessage_channelID, client=client, before=before, after=after, row=row, sheetData=sheetData, member_point=member_point)

		pass


	async def on_member_join( self, config, client: discord.Client, member: discord.Member ) :
		#print("test member join")
		pass