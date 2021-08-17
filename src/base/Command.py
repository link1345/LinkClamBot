import discord
from discord.ext import tasks

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
	

	async def reload(self, client: discord.Client) :
		CPrint.warning_print(" ----------- Module Reload ----------- ")
		try :
			# まずはタスク全消し。
			self.removeTask()

			# 設定リロード
			importlib.reload(CommandSet)
			self.C_list = CommandSet.CommandList

			# 追加モジュールリロード
			for key in self.C_list.keys() :	
				if  self.C_list[key].get("Add_Module") is None :
					continue
				
				for module in self.C_list[key]["Add_Module"] :
					importlib.reload( importlib.import_module( module ) )


			# 通常モジュール取得
			self.Commandimport(mode="reload")
			
			# タスクイベント リロード
			self.setTask(client)


			CPrint.success_print(" ------- Success Module Reload ------- ")
			return True
		except :
			CPrint.error_print(  " -------- Error Module Reload -------- ")
			
			import traceback
			traceback.print_exc()
			return False


	def Commandimport(self, mode="defule"):
		for key in self.C_list.keys() :	
			self.C_list[key]["module"] = importlib.import_module( self.C_list[key]["PythonFile"])

			if mode == "reload" :
				importlib.reload( self.C_list[key]["module"] )

			self.C_list[key]["object"] = self.C_list[key]["module"].command()
		#print ( self.C_list )

# ------------------------------------------------------------------
# ------------------------------------------------------------------

	def setTask(self, client: discord.Client):
		for key in self.C_list :
			taskData = self.C_list[key].get("on_task")
			if taskData is not None :
				for taskkey in taskData :
					# タスク関数を取得
					func = getattr( self.C_list[key]["object"] , taskkey )
					self.C_list[key]["on_task"][taskkey]["func"] = func

					# hours
					timelist = ["hours" , "minutes" , "seconds"]
					timedata = []
					for timeitem in timelist :
						timedata.append( self.C_list[key]["on_task"][taskkey].get(timeitem) )
					
					# 実行内容
					self.C_list[key]["on_task"][taskkey]["task"] = ( tasks.loop(hours=timedata[0] , minutes=timedata[1],seconds=timedata[2] ))( self.C_list[key]["on_task"][taskkey]["func"] )
					self.C_list[key]["on_task"][taskkey]["task"].start( config=self.C_list[key], client=client )

		pass
	

	def removeTask(self):
		for key in self.C_list :
			taskData = self.C_list[key].get("on_task")
			if taskData is not None :
				for taskkey in taskData :

					# ストップ!
					if self.C_list[key]["on_task"][taskkey].get("task") is not None :
						self.C_list[key]["on_task"][taskkey]["task"].stop()

		pass

# ------------------------------------------------------------------
# ------------------------------------------------------------------

	async def on_message(self, client: discord.Client, message: discord.Message):
		
		async def run( key: str, client: discord.Client, message: discord.Message ):
			try :
				await self.C_list[key]["object"].on_message(config=self.C_list[key], client=client, message=message)
			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass

		for key in self.C_list :
			# メッセージ設定が無ければ、そのまま通す. [bot判定なし]
			if self.C_list[key].get("onMessage") is None :
				await run(key, client, message)
				continue
			
			if Sendtool.bot_check(message.author) :
				#print("BOT!")
				continue

			if self.C_list[key]["object"].talk is True :
				await run(key, client, message)
				continue

			# 以降[Bot判定あり]

			run_Flag = [] # Max=3

			# 命令チェック
			c_text = self.C_list[key]["onMessage"].get("CommandText")
			if c_text is None :
				run_Flag.append("Text")
			else :				
				for item_text in c_text :
					check_cotent = client.user.display_name + item_text
					if check_cotent ==  message.content :
						run_Flag.append("Text")
						break
			
			# ChannelIDチェック
			c_channel = self.C_list[key]["onMessage"].get("channelID")
			if c_channel is None :
				run_Flag.append("Channel") ## ここ確認
			else :
				if message.channel.id in c_channel : 
					run_Flag.append("Channel")

			# ロールチェック
			c_role = self.C_list[key]["onMessage"].get("role")
			if c_role is None :
				run_Flag.append("role")
			else :
				for item_role in message.author.roles:
					if item_role.id in c_role :
						run_Flag.append("role")
						break

			# ALLチェック完了 run
			#print("flag : " +  str(run_Flag) + "  content:" + message.content )
			if len(run_Flag) == 3 :
				await run(key, client, message)


	async def on_ready(self, client: discord.Client ):
		async def run( key: str, client: discord.Client ):
			try:
				await self.C_list[key]["object"].on_ready(config=self.C_list[key], client=client)
			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass
	
		# Bot起動後にタスク読み込み
		self.setTask(client)

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
						await self.reload(client)

			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass

		for key in self.C_list :
			await run(key , client=client,  interaction=interaction)


	async def on_member_update(self, client: discord.Client, before: discord.Member, after: discord.Member):
		pass


	async def on_member_remove(self, client: discord.Client, member: discord.Member ):
		pass


	async def on_user_update(self, client: discord.Client, before: discord.User, after: discord.User):
		pass


	async def on_voice_state_update(self, client: discord.Client, member: discord.Member, before: discord.VoiceState , after: discord.VoiceState):
		async def run( key: str, client: discord.Client , member: discord.Member, before: discord.VoiceState , after: discord.VoiceState):
			try:
				await self.C_list[key]["object"].on_voice_state_update(config=self.C_list[key], client=client, member=member, before=before , after=after)
			except AttributeError:
				# イベント先がない場合は、スルーする。
				pass
	
		for key in self.C_list :
			await run(key , client=client, member=member, before=before , after=after)
		pass
