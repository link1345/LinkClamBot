import discord
from discord.ext import tasks

from datetime import datetime, timedelta
import urllib.parse
import os
import sys
import importlib

import functools 

import config.BaseSetting # token 設定場所
import base.DiscordSend as Sendtool


#class test_task(tasks.Loop) :
#	def __init__(self):
#		#super().__init__('coro', 'seconds', 'hours', 'minutes', 'time', 'count', 'reconnect', and 'loop')
#		self.seconds = 10
	
#	async def __call__(self , *args, **kwargs):
#		print("test")


class LinkClanBot :

	def __init__(self):

		intents = discord.Intents.default()
		intents.members = True
		intents.guilds = True

		self.client = discord.Client(intents=intents)


		#self.test_task = tasks.Loop()
		#self.test_task.seconds = 10

		self.EventSet()	

		print( type(self) )


	def run(self) :
		self.client.run(config.BaseSetting.BotToken)

	def EventSet(self) :
	
		@self.client.event
		async def on_message(message: discord.Message):
			#await message.channel.send("test")
			await Sendtool.Send(message, "test")
			pass

		@self.client.event
		async def on_ready():
			pass
		
		@self.client.event
		async def on_member_remove(member):
			pass
		
		@self.client.event
		async def on_member_update(before, after):
			pass
		
		@self.client.event
		async def on_user_update(before, after):
			pass

		@self.client.event
		async def on_voice_state_update(member, before, after):
			pass

		async def test(text: str):
			print("test " + text)

		test_task = (tasks.loop(seconds=5))(test)
		test_task.start("hello")

		#self.test_task.__call__ = test
		#self.test_task.start()
