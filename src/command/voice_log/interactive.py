

import discord
import base.command_base as base

import base.DiscordSend as Sendtool

import command.voice_log.Config_Main as CSetting

class test_button_Button(discord.ui.Button['test_button']):

	def __init__(self, text: str, client, clientData, config):
		super().__init__(label=text, style=discord.ButtonStyle.secondary)

		self.client = client
		self.clientData = clientData
		self.config = config

		self.Send_ChannelID = self.config.CommandList["INTERACITVE_VOICE_LOG"]["onMessage"]["channelID"]
		print(self.Send_ChannelID)
		pass

	async def item_stop(self , interaction: discord.Interaction):
		# ボタン無効
		assert self.view is not None
		view: test_button = self.view

		self.disabled = True
		for child in view.children:
			assert isinstance(child, discord.ui.Button)
			child.disabled = True
		return view.stop()

		
	async def callback(self, interaction: discord.Interaction) :

		if self.label == "現行ログ" :
			self.clientData.time_mode = "now"

			assert self.view is not None
			view: test_button = self.view
			view.clear_items()
			view.add_item(test_button_Button("生ログ", self.client, self.clientData))
			view.add_item(test_button_Button("加工済みログ", self.client, self.clientData))

			text = "どちらの形式のデータを取得したいですか？"
			await interaction.response.edit_message(content=text, view=view)
		elif self.label == "過去ログ" :
			self.clientData.time_mode = "old"
			print("過去ログ")

		elif self.label == "生ログ" and self.clientData.time_mode == "now" :	
			print("生ログ・now")

			now_filepath = CSetting.baseLogFolder + CSetting.JSONPATH_row + CSetting.JSONPATH_now
			text = "現行の音声チャンネルログイン生データです"
			await interaction.response.edit_message(content="aaa", view=None)
			await Sendtool.Send_ChannelID(client=self.client, channelID=self.Send_ChannelID, message=text, filename=now_filepath)


		elif self.label == "生ログ" and self.clientData.time_mode == "old" :
			print("生ログ・old")

		elif self.label == "加工済みログ" and self.clientData.time_mode == "now" :
			print("加工済みログ・now")

			# 計算済みファイル		
			timeData = await Chart.makeTimeList(client, now_filepath , CSetting.OneMonthOutput_RoleID , mode="NAME")
			if timeData is not None :
				send_fileName = CSetting.baseLogFolder + CSetting.JSONPATH_row + CSetting.JSONPATH_now_csv
				timeData.to_csv( send_fileName )
			
				text = "現行の音声チャンネルログイン生データです"
				await interaction.response.edit_message(content="aa", view=None)
				await Sendtool.Send_ChannelID(client=self.client, channelID=self.Send_ChannelID, message=text, filename=send_fileName)
			else : 
				text = "現行の音声チャンネルログイン加工済みデータを作成できませんでした"
				await interaction.response.edit_message(content="aa", view=None)
				await Sendtool.Send_ChannelID(client=self.client, channelID=self.Send_ChannelID, message=text, filename=None)



		elif self.label == "加工済みログ" and self.clientData.time_mode == "old" :
			print("加工済みログ・old")

		# ボタン無効
		#view = self.item_stop()
		#await interaction.response.edit_message(view=view)

		pass


class test_button(discord.ui.View):
	def __init__(self, args: list[str], client, clientData, config):
		super().__init__()

		self.button = []

		for item in args :
			self.button.append(test_button_Button(item, client, clientData, config))
			self.add_item(self.button[-1])



class command(base.command_base)  :

	def __init__(self) :
		super().__init__()

		self.time_mode = "now"
		self.send_mode = "row"

		pass

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		print("test")

		self.eventButton = test_button(["過去ログ","現行ログ"], client=client ,clientData=self , config=config )
		await Sendtool.Send_Member(Data=message, message="どのような", filename=None,view=self.eventButton)

		# よくわからないが。なんかうごかない！
		

		#await Sendtool.Send_Member(Data=message, message="ログファイルがありませんでした。", filename=None)