
import discord
import base.DiscordSend as Sendtool

import base.command_base as base


from discord.ext import tasks


class command(base.command_base)  :

	def __init__(self) :
		super().__init__()
		#self.test_task: tasks.Loop = None

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		
		await Sendtool.Send_Member(Data=message, message="test message", filename=None)

		#async def test(text: str, client: discord.Client, channelID: int):
		#	await Sendtool.Send_ChannelID(client, channelID, "TASK")
		#
		#if self.test_task is None :
		#	self.test_task = (tasks.loop(seconds=5,count=3))(test)
		#	self.test_task.start("hello", client, message.channel.id)
		#elif self.test_task.is_running() :
		#	self.test_task.stop()
		#	await Sendtool.Send_Member(Data=message, message="task stop", filename=None)

		pass

	#async def on_ready(self, config, client: discord.Client):
	#	print("HELLO! Ready")