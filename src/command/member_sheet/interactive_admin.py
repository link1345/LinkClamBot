
import sys

import discord
from discord.ext import tasks

import command.member_sheet.interactive_user as inter_user

import base.DiscordSend as Sendtool
import command.member_sheet.Config_Main as CSetting
import command.member_sheet.GoogleSheet as CSheet

import pandas as pd
import math

from discord.ext import tasks

import copy

class push_Button(discord.ui.Button['ListMenu']):

	def __init__(self, data, text: str):
		super().__init__(label=text, style=discord.ButtonStyle.secondary)
		self.data = data

	async def callback(self, interaction: discord.Interaction) :
		if self.label == "決定" :
			self.data.talkNum_admin = 1 
			await interaction.message.delete()

			# 聞いて置く。(この後、対話があるが、ここではやっていない。)
			print( "point" , self.data.SelectPoint , "   num:", self.data.SelectPoint + ( 25 * self.data.SelectListPoint ) )

			userID = self.data.col[self.data.SelectPoint + ( 25 * self.data.SelectListPoint ) ]
			self.data.SelectUser = self.data.client.get_user( int(userID) )
			await self.data.interactive(self.data.client, message=self.data.message, member=self.data.SelectUser)
		return

class ListMenu_SelectMenu(discord.ui.Select['ListMenu']):

	def __init__(self, data, text: list[str], mode="MemberName"):
		super().__init__()

		self.text = text
		self.data = data
		self.mode = mode

		#print("custom_id : ", self.custom_id )
		if mode == "MemberName" :
			start_num = 25 * self.data.SelectListPoint
			stop_num = 0
			if ( len(self.text) / 25 - self.data.SelectListPoint ) > 1.0 :
				stop_num = 25 * self.data.SelectListPoint + 1
			else :
				stop_num = ( len(self.text) ) % 25 + ( 25 * self.data.SelectListPoint )

			print( "start:" , start_num , "   stop:" , stop_num )
			for item_num in range( start_num , stop_num) :
				print("num : " , item_num)
				defaultFlag = False
				if item_num == start_num :
					defaultFlag = True
				#print("add " , item )
				self.add_option(label=text[item_num], default=defaultFlag)
		else :
			num = 0
			for item in text :
				defaultFlag = False
				if num == 0 :
					defaultFlag = True
				#print("add " , item )
				self.add_option(label=item, default=defaultFlag)
				num += 1
			



	async def callback(self, interaction: discord.Interaction):
		view: TicTacToe = self.view
		
		if self.mode == "Numberlist" :
			self.data.SelectListPoint = self.text.index( self.values[-1] )

			for child in view.children:
				if not isinstance(child, discord.ui.Select) :
					continue
				if child.custom_id != self.custom_id :
					view.remove_item(child)
					view.add_item( ListMenu_SelectMenu(data, self.data.select_message) )
			
			await interaction.message.edit(view=view)

		elif self.mode == "MemberName" :
			self.data.SelectPoint = self.text.index( self.values[-1] )
		#print("put")
		pass

class ListMenu(discord.ui.View):

	def __init__(self, data,text: list[str]):
		super().__init__()

		membarlist = []
		for num in range( math.ceil( len(text) / 25 ) ) :
			membarlist.append( "list : " + str(num + 1) )
		self.add_item(ListMenu_SelectMenu(data, membarlist, mode="Numberlist" ))
		self.add_item(ListMenu_SelectMenu(data,text))
		self.add_item(push_Button(data,"決定"))
		


class command(inter_user.command)  :

	def __init__(self) :
		super().__init__()

		self.talk = False
		self.talk_UserID = 0
		self.talkNum_admin = 0

		self.button_reset()

		pass

	def button_reset(self) :

		self.eventButton = None

		self.SelectListPoint = 0
		self.SelectPoint = 0
		self.SelectUser = None

		self.col = []
		self.displayName_col = []
		self.select_message = []
	
		self.client = None
		self.message = None
	

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		self.client = client
		self.message = message

		if self.talkNum_admin == 0 :	
			worksheet = CSheet.getGooglesheet()

			self.col , self.displayName_col = CSheet.getIndex_AllMember(worksheet, self.CSet_index_list, self.Flag_discord_Member)

			for num in range(len(self.displayName_col)) :
				self.select_message.append(  self.displayName_col[num] + "  (" + client.get_user( int(self.col[num]) ).name + "#" + client.get_user( int(self.col[num]) ).discriminator + ")" )
			#self.eventButton = ListMenu( self, self.displayName_col )
			self.eventButton = ListMenu( self, self.select_message )
			
			#print("displayName_col " , self.displayName_col)
			#print("col " , self.col)

			await Sendtool.Send_Member(Data=message, message="誰の名簿情報を変更しますか？", view=self.eventButton)
			print("test!")
		
		# "決定ボタンを押した後"
		elif self.talkNum_admin == 1 :
			#print("admin!")
			if await self.interactive(self.client, message=message, member=self.SelectUser) :
				self.talkNum_admin = 0				
				self.button_reset()			
			#await Sendtool.Send_Member(Data=message, message="interactive test message", filename=None)

		pass