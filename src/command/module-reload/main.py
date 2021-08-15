
import discord
import base.DiscordSend as Sendtool

import base.command_base as base

class test_button_Button(discord.ui.Button['test_button']):

	def __init__(self, text: str, client: discord.Client, ReloadFlag: bool):
		super().__init__(label=text, style=discord.ButtonStyle.secondary)

		#self.client = client
		#self.ReloadFlag = ReloadFlag

	#async def callback(self, interaction: discord.Interaction) :

		#self.style = discord.ButtonStyle.red

		#for child in self.view.children:
		#	child.disabled = True

		#self.disabled = True
		#self.ReloadFlag = True

		#await Sendtool.Send_ChannelID(client=self.client, channelID=interaction.channel_id, message="モジュールリロードします。", filename=None)
		#self.view.stop()



class test_button(discord.ui.View):
	def __init__(self, args: list[str], client: discord.Client, ReloadFlag: bool):
		super().__init__()

		self.button = []

		for item in args :
			self.button.append(test_button_Button(item, client, ReloadFlag))
			self.add_item(self.button[-1])


class command(base.command_base) :

	def __init__(self) :
		super().__init__()
		self.ReloadFlag = False
		self.eventButton : test_button


	async def on_message(self, config, client: discord.Client, message: discord.Message) :			
		
		self.eventButton = test_button(["YES","NO"], client=client, ReloadFlag=self.ReloadFlag)
		await Sendtool.Send_Member(Data=message, message="本当にモジュールをリロードしますか？", filename=None,view=self.eventButton)


		# この後、Base.Commandの方で直でリロード処理掛けます。	
		pass

	async def on_interaction(self, config, client: discord.Client, interaction: discord.Interaction):
		if await self.eventButton.interaction_check( interaction ) :

			self.ReloadFlag = True
			print("OK reload command")
		
			#await interaction.delete_original_message()
			
			await interaction.edit_original_message(content="【報告】モジュールをリロードしました。", view=None)
			

		pass