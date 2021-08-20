
import sys

import discord
from discord.ext import tasks

import command.member_sheet.interactive_user as inter_user

import base.DiscordSend as Sendtool
import command.member_sheet.Config_Main as CSetting
import command.member_sheet.GoogleSheet as CSheet

import pandas as pd

from discord.ext import tasks

import copy

class push_Button(discord.ui.Button['ListMenu']):

	def __init__(self, data, text: str):
		super().__init__(label=text, style=discord.ButtonStyle.secondary)
		self.data = data

	async def callback(self, interaction: discord.Interaction) :
		if self.label == "決定" :
			self.data.talkNum_admin = 1 
			assert self.view is not None
			view: ListMenu = self.view
			view.clear_items()
			await interaction.message.delete()

			# 聞いて置く。(この後、対話があるが、ここではやっていない。)
			userID = self.data.col[self.data.SelectPoint]
			self.data.SelectUser = self.data.client.get_user( int(userID) )
			await self.data.interactive(self.data.client, message=self.data.message, member=self.data.SelectUser)

		return

class ListMenu_SelectMenu(discord.ui.Select['ListMenu']):

	def __init__(self, data, text: list[str]):
		super().__init__()

		self.text = text
		self.data = data

		num = 0
		for item in text :
			defaultFlag = False
			if num == 0 :
				defaultFlag = True
			print("add " , item )
			self.add_option(label=item, default=defaultFlag)
			num += 1

	async def callback(self, interaction: discord.Interaction):
		#view: ListMenu = self.view
		self.data.SelectPoint = self.text.index( self.values[-1] )
		print("put")
		pass

class ListMenu(discord.ui.View):

	def __init__(self, data,text: list[str]):
		super().__init__()
		self.add_item(ListMenu_SelectMenu(data,text))
		self.add_item(push_Button(data,"決定"))


class command(inter_user.command)  :

	def __init__(self) :
		super().__init__()

		self.talk = False
		self.talk_UserID = 0
		self.talkNum_admin = 0

		self.eventButton = None

		self.SelectPoint = 0
		self.SelectUser = None

		self.col = []
		self.displayName_col = []
	
		self.client = None
		self.message = None

		pass

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		self.client = client
		self.message = message

		if self.talkNum_admin == 0 :	
			worksheet = CSheet.getGooglesheet()

			self.col , self.displayName_col = CSheet.getIndex_AllMember(worksheet, self.CSet_index_list, self.Flag_discord_Member)
			self.eventButton = ListMenu( self, self.displayName_col )
			
			#print("displayName_col " , self.displayName_col)
			#print("col " , self.col)

			await Sendtool.Send_Member(Data=message, message="誰の名簿情報を変更しますか？", view=self.eventButton)
		
		# "決定ボタンを押した後"
		elif self.talkNum_admin == 1 :
			#print("admin!")
			if await self.interactive(self.client, message=message, member=self.SelectUser) :
				self.talkNum_admin = 0				
			#await Sendtool.Send_Member(Data=message, message="interactive test message", filename=None)

		pass