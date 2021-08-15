
import discord
import base.DiscordSend as Sendtool

import base.command_base as base

class command(base.command_base)  :

	def __init__(self) :
		super().__init__()

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		if Sendtool.bot_check(message.author) :
			return
		
		await Sendtool.Send_Member(Data=message, message="hello!___world test message", filename=None)
		#print("test sample")

		pass

	#async def on_ready(self, config, client: discord.Client):
	#	print("HELLO! Ready")