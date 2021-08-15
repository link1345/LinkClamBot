import discord
from discord.ext import tasks

import functools 

import config.BaseSetting # token 設定場所

import base.Command as Command

import base.DiscordSend as Sendtool

class LinkClanBot :

	def __init__(self):

		intents = discord.Intents.default()
		intents.members = True
		intents.guilds = True

		self.client = discord.Client(intents=intents)

		self.command = Command.DiscordCommand()
		self.command.Commandimport()

		self.EventSet()	


	def run(self) :
		self.client.run(config.BaseSetting.BotToken)

	def EventSet(self) :
	
		text = "test1"

		@self.client.event
		async def on_message(message: discord.Message):
			await self.command.on_message(self.client, message)
			pass

		@self.client.event
		async def on_ready():
			await self.command.on_ready(self.client)
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

		@self.client.event
		async def on_interaction(interaction: discord.Interaction ):
			await self.command.on_interaction(self.client, interaction)
			pass

		#async def test(text: str):
		#	print("test " + text)

		#test_task = (tasks.loop(seconds=5))(test)
		#test_task.start("hello")
		