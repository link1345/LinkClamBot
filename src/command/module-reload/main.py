
import discord
import base.DiscordSend as Sendtool

import base.command_base as base

class test_button_Button(discord.ui.Button['test_button']):

	def __init__(self, text: str, client, clientData):
		super().__init__(label=text, style=discord.ButtonStyle.secondary)

		self.clientData = clientData
		self.client = client
		
	async def callback(self, interaction: discord.Interaction) :

		if self.label == "YES" :
			self.clientData.ReloadFlag = True
			await Sendtool.Send_ChannelID(client=self.client, channelID=interaction.channel_id, message="モジュールリロードします。")
		else :
			await Sendtool.Send_ChannelID(client=self.client, channelID=interaction.channel_id, message="モジュールリロードしませんでした")

		# ------------

		assert self.view is not None
		view: test_button = self.view

		self.disabled = True
		for child in view.children:
			assert isinstance(child, discord.ui.Button) # just to shut up the linter
			child.disabled = True

		view.stop()

		# ボタン受付を禁止したViewを反映させる		
		await interaction.response.edit_message(view=view)
		
		pass


class test_button(discord.ui.View):
	def __init__(self, args: list[str], client, clientData):
		super().__init__()

		self.button = []

		#clientData.ReloadFlag = True

		for item in args :
			self.button.append(test_button_Button(item, client, clientData))
			self.add_item(self.button[-1])


class command(base.command_base) :

	def __init__(self) :
		super().__init__()
		self.ReloadFlag = False
		self.eventButton : test_button

	async def on_message(self, config, client: discord.Client, message: discord.Message) :			
		
		self.eventButton = test_button(["YES","NO"], client=client ,clientData=self )
		await Sendtool.Send_Member(Data=message, message="本当にモジュールをリロードしますか？", filename=None,view=self.eventButton)
		
		# この後、Base.Commandの方で直でリロード処理掛けます。	
		pass

	async def on_interaction(self, config, client: discord.Client, interaction: discord.Interaction):
		# module-reloadは、ここでは何もしない。
		# 上位の関数で、reload処理をかけている。
		pass