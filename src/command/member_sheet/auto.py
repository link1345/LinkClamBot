
import sys

import discord
from discord.ext import tasks

import base.command_base as base
import base.DiscordSend as Sendtool
import command.member_sheet.Config_Main as CSetting

import command.member_sheet.GoogleSheet as CSheet

import gspread
import pandas as pd

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
			num = CSetting.SheetIndex.index(s_index) + 1
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


	def getIndex(self, worksheet: gspread.Spreadsheet, member: discord.Member):
		# return は、 「行(member.idが当てはまる行)」 , 「列(col discordID部分)」 

		row_index = worksheet.row_values(1)
		#if not Check_ConfigList( row_index ) :
		if set(row_index) != set(self.CSet_index_list) :
			return None, None

		# ID(列)を取得
		col = worksheet.col_values(self.Flag_discord_Member_id)

		member_point = None
		if member.id in col:
			try :
				member_point = col.index(member.id)
			except IndexError:
				print("名簿にいません")

		row = None
		if member_point is not None :
			row = worksheet.row_values(member_point)
		
		return row, col , member_point

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		await Sendtool.Send_Member(Data=message, message="auto test message", filename=None)


	async def change_memberData(self, client: discord.Client, before: discord.Member, after: discord.Member):
		pass
	
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
			row, col, member_point = self.getIndex(sheetData, after)
			print("row : " , row)
			print("col : " , col)

			if row is None and col is None :
				text = "**【ERROR】**Botで設定されているindexとGoogleSheetのindexが違います。修正お願い致します。"
				await Sendtool.Send_ChannelID(client=client, channelID=CSetting.AutoEvent_ERRORMessage_channelID, message=text, filename=None)
			
			if member_point is None :
				# 名簿に存在しないので、新規登録
				

		pass


	async def on_member_remove( self, config, client: discord.Client, member: discord.Member ) :
		print("test member remove")
		pass

	async def on_user_update( self, config, client: discord.Client, before: discord.User, after: discord.User ) :
		print("test user update")
		pass

	async def on_member_join( self, config, client: discord.Client, member: discord.Member ) :
		print("test member join")
		pass