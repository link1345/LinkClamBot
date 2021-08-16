
import sys

import discord
import base.DiscordSend as Sendtool

import base.command_base as base


from discord.ext import tasks


class command(base.command_base)  :

	def __init__(self) :
		super().__init__()
		self.test_task: tasks.Loop = None

	#async def on_message(self, config, client: discord.Client, message: discord.Message) :
	#	pass

	#async def on_ready(self, config, client: discord.Client):
	#	print("HELLO! Ready")

	async def voice_log(self, config, client: discord.Client):
		
		channellist = []
		if config.get("on_task") is not None :
			if config["on_task"].get(sys._getframe().f_code.co_name) is not None :
				channellist = config["on_task"][sys._getframe().f_code.co_name].get("message-channelID")
				
		if channellist is None :
			return 

		for ID in channellist :
			await Sendtool.Send_ChannelID(client=client, channelID=int(ID), message="TASK")
		
		pass