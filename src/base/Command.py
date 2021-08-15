import discord

import os

#from datetime import datetime, timedelta
#import sys

import pathlib
import importlib

import base.ColorPrint as CPrint

import config.CommandSetting as CommandSet

import base.DiscordSend as Sendtool

class DiscordCommand :

	def __init__(self) :
		#self.root_command_folder = "./opt/command"
		self.C_list = CommandSet.CommandList
	
	async def reload(self) :
		CPrint.warning_print(" ----------- Module Reload ----------- ")
		try :
			for key in self.C_list.keys() :
				importlib.reload(self.C_list[key]["module"])
				self.C_list[key]["object"] = self.C_list[key]["module"].command()
			
			CPrint.success_print(" ------- Success Module Reload ------- ")
			return True
		except :
			
			CPrint.error_print(  " -------- Error Module Reload -------- ")
			return False



	def Commandimport(self):
		for key in self.C_list.keys() :
			#print( key )
			self.C_list[key]["module"] = importlib.import_module( self.C_list[key]["PythonFile"])
			self.C_list[key]["object"] = self.C_list[key]["module"].command()
		#print ( self.C_list )

	async def on_message(self, client: discord.Client, message: discord.Message):
		
		async def run( key: str, client: discord.Client, message: discord.Message ):
			try :
				await self.C_list[key]["object"].on_message(config=self.C_list[key], client=client, message=message)

				#if key == "RELOAD" :
				#	if self.C_list[key]["object"].ReloadFlag :
				#		self.C_list[key]["object"].ReloadFlag = False
				#		await self.reload()

			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass

		for key in self.C_list :
			# メッセージ設定が無ければ、そのまま通す. [bot判定なし]
			if self.C_list[key].get("onMessage") == None :
				await run(key, client, message)
				continue
			
			if Sendtool.bot_check(message.author) :
				#print("BOT!")
				continue

			if self.C_list[key]["object"].talk == True :
				await run(key, client, message)
				continue

			# 以降[Bot判定あり]

			run_Flag = [] # Max=3
			
			# 命令チェック
			c_text = self.C_list[key]["onMessage"].get("CommandText")
			if c_text == None :
				run_Flag.append("Text")
			for item_text in c_text :
				check_cotent = client.user.display_name + item_text
				if check_cotent ==  message.content :
					run_Flag.append("Text")
					break
			
			# ChannelIDチェック
			c_channel = self.C_list[key]["onMessage"].get("channelID")
			if c_channel == None :
				run_Flag.append("Channel")
			for item_channel in c_channel :
				if str(message.channel.id) == item_channel :
					run_Flag.append("Channel")
					break

			# ロールチェック
			c_role = self.C_list[key]["onMessage"].get("role")
			if c_role == None :
				run_Flag.append("role")
			
			c_role_flag = False
			for item_role in c_role :
				for user_role in message.author.roles :
					if item_role == user_role.name :
						c_role_flag = True
						run_Flag.append("role")
						break
				
				if c_role_flag == True :
					break

			# ALLチェック完了 run
			#print("flag : " +  str(run_Flag)  )
			if len(run_Flag) == 3 :
				await run(key, client, message)


	async def on_ready(self, client: discord.Client ):
		async def run( key: str, client: discord.Client ):
			try:
				await self.C_list[key]["object"].on_ready(config=self.C_list[key], client=client)
			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass
	
		for key in self.C_list :
			await run(key , client=client)
		
		pass
	

	async def on_interaction(self, client: discord.Client, interaction: discord.Interaction):
		
		async def run( key: str, client: discord.Client, interaction: discord.Interaction ):
			try :
				await self.C_list[key]["object"].on_interaction(config=self.C_list[key], client=client, interaction=interaction)

				if key == "RELOAD" :
					if self.C_list[key]["object"].ReloadFlag :
						self.C_list[key]["object"].ReloadFlag = False
						await self.reload()

			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass

		for key in self.C_list :
			await run(key , client=client,  interaction=interaction)