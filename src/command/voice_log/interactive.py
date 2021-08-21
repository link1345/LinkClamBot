

import discord
import base.command_base as base

import base.DiscordSend as Sendtool
import command.voice_log.chart as Chart

import command.voice_log.Config_Main as CSetting

class Role_Menu_SelectMenu(discord.ui.Select['ListMenu']):

	def __init__(self, text: list[str], description: list[str], guildList: list[str],roleList: list[str], clientData):
		super().__init__()

		self.list = text
		self.clientData = clientData
		self.roleList = roleList
		self.guildList = guildList
	
		self.clientData.roleID = self.roleList[0]
		self.clientData.roleName = self.list[0]

		for item in text :
			defaultFlag = False
			num = text.index(item)
			if num == 0 :
				defaultFlag = True
			self.add_option(label=item, description=description[num] , default=defaultFlag)

	async def callback(self, interaction: discord.Interaction):
		#print("value : " , self.values )
		self.clientData.roleID = self.roleList[ self.list.index( self.values[-1] ) ]
		self.clientData.guildID = self.guildList[ self.list.index( self.values[-1] ) ]
		self.clientData.roleName = self.list[ self.list.index( self.values[-1] ) ]
		#print("id : " , self.clientData.roleID )


class Month_Menu_SelectMenu(discord.ui.Select['ListMenu']):

	def __init__(self, text: list[str], clientData):
		super().__init__()

		self.list = text
		self.clientData = clientData

		for item in text :
			defaultFlag = False
			num = text.index(item)
			if num == 0 :
				defaultFlag = True
			self.add_option(label=item, default=defaultFlag)

	async def callback(self, interaction: discord.Interaction):
		#print("value : " , self.values )
		self.clientData.Months = self.list.index( self.values[-1] ) + 1
		#print("id : " , self.clientData.Months )


class test_button_Button(discord.ui.Button['test_button']):

	def __init__(self, text: str, client, clientData, config):
		super().__init__(label=text, style=discord.ButtonStyle.secondary)

		self.client = client
		self.clientData = clientData
		self.config = config
		#self.Send_ChannelID = self.config["onMessage"]["channelID"]
		pass

	def item_stop(self , interaction: discord.Interaction):
		# ボタン無効
		assert self.view is not None
		view: test_button = self.view

		self.disabled = True
		for child in view.children:
			assert isinstance(child, discord.ui.Button)
			child.disabled = True
		return view.stop()

		
	async def callback(self, interaction: discord.Interaction) :
		
		async def interactive2_button() :
			assert self.view is not None
			view: test_button = self.view
			view.clear_items()
			view.add_item(test_button_Button("生ログ", self.client, self.clientData, self.config))
			view.add_item(test_button_Button("加工済みログ", self.client, self.clientData, self.config))

			text = "どちらの形式のデータを取得したいですか？"
			await interaction.response.edit_message(content=text, view=view)
		
		async def interactive3_old_button() :
			assert self.view is not None
			view: test_button = self.view
			view.clear_items()

			roleList = []
			guildList = []
			roleIDList = []
			printLabel_roleList = []
			printText_roleList = []
			for guild_item in self.client.guilds :
				await guild_item.chunk()
				roleList += guild_item.roles

				for role_item in guild_item.roles :
					roleIDList.append(role_item.id)
					guildList.append(guild_item.id)
					printLabel_roleList.append( guild_item.name + "の役職「" + role_item.name + "」" )
					printText_roleList.append( "Role ID : " + str( role_item.id )  )

			view.add_item( Role_Menu_SelectMenu( printLabel_roleList, printText_roleList, guildList, roleIDList, self.clientData) )
			view.add_item( test_button_Button("決定", self.client, self.clientData, self.config) )

			await interaction.response.edit_message(content="取得したいロールを決めてください。", view=view)
			#text = "どの役職のデータを取得しますか？"
			#await interaction.response.edit_message(content=text, view=view)

		async def interactive4_old_button() :
			assert self.view is not None
			view: test_button = self.view
			view.clear_items()
			# 
			# ここでSelectMenuを作る
			old_month, self.clientData.labellist, self.clientData.fileNameList = Chart.most_old_Month()

			if old_month == 0 :
				return False

			view.add_item( Month_Menu_SelectMenu( self.clientData.labellist, self.clientData) )
			view.add_item( test_button_Button("決定", self.client, self.clientData, self.config) )
			await interaction.response.edit_message(content= "何か月までのデータを取得しますか？", view=view)
			return True


		if self.label == "現行ログ" :
			self.clientData.time_mode = "now"
			await interactive2_button()

		elif self.label == "過去ログ" :
			self.clientData.time_mode = "old"
			await interactive3_old_button()

		# 現在のログ出力関係
		elif self.label == "生ログ" and self.clientData.time_mode == "now" :

			now_filepath = CSetting.baseLogFolder + CSetting.JSONPATH_row + CSetting.JSONPATH_now
			text = "現行の音声チャンネルログイン生データです"
			await interaction.message.delete()
			await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text, filename=now_filepath)
			## 諸処初期化
			self.clientData.reset()

		elif self.label == "加工済みログ" and self.clientData.time_mode == "now" :

			# 計算済みファイル	
			now_filepath = CSetting.baseLogFolder + CSetting.JSONPATH_row + CSetting.JSONPATH_now
			timeData = await Chart.makeTimeList(self.client, now_filepath , CSetting.OneMonthOutput_RoleID , mode="NAME")
			if timeData is not None :
				send_fileName = CSetting.baseLogFolder + CSetting.JSONPATH_analysis + CSetting.JSONPATH_now_csv
				timeData.to_csv( send_fileName )
			
				text = "現行の音声チャンネルログイン生データです"
				await interaction.message.delete()
				await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text, filename=send_fileName)
			else : 
				text = "現行の音声チャンネルログイン加工済みデータを作成できませんでした"
				await interaction.message.delete()
				await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text)
			## 諸処初期化
			self.clientData.reset()

		# 過去のログ出力関係
		elif self.label == "決定" and not self.clientData.oldMode_Role_ok and not self.clientData.oldMode_Month_ok :
			#print("OK oldMode_Role_ok")
			self.clientData.oldMode_Role_ok = True
			if await Chart.UserRoleMember( client=self.client, RoleList=[self.clientData.roleID] ) == [] :
				text = "指定された" +  self.clientData.roleName + "には、誰も所属していません。"
				await interaction.message.delete()
				await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text)
				self.clientData.reset()
				return 

			if not await interactive4_old_button() :
				# 過去ログが無ければ...ここで終わりにする。
				text = "過去ログが存在しないため、出力出来ません。"
				await interaction.message.delete()
				await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text)
				self.clientData.reset()
				return 


		elif self.label == "決定" and self.clientData.oldMode_Role_ok and not self.clientData.oldMode_Month_ok :
			#print("OK oldMode_Role_ok and oldMode_Month_ok  csv出力するで～")
			self.clientData.oldMode_Role_ok = True

			#print("list : " , self.clientData.fileNameList[0:self.clientData.Months])

			timeData = await Chart.makeOldTimeList(client=self.client, MonthFileList=self.clientData.fileNameList[0:self.clientData.Months], IndexLabel=self.clientData.labellist[0:self.clientData.Months], RoleList=[self.clientData.roleID])
			if timeData is not None :
				# 終わりに...		
				send_fileName = CSetting.baseLogFolder + CSetting.JSONPATH_analysis + CSetting.JSONPATH_old_csv
				timeData.to_csv( send_fileName )

				text = "過去の音声チャンネルログインデータ(加工済み)です"
				await interaction.message.delete()
				await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text, filename=send_fileName)

				# -------

				#waring_timeData = timeData.drop(columns=['name'])
				waring_timeData = timeData

				for user in waring_timeData.index.values :
					waringNum = 0
					for value in waring_timeData.columns.values :
						if value == 'name' :
							continue
						if waring_timeData.loc[user, value] >= CSetting.WaringTime :
							break
						waringNum += 1
					if not waringNum > CSetting.WaringMonths :
						waring_timeData.drop(index=[user])

				waring_timeData.to_csv( send_fileName )

				if len(waring_timeData.index.values) != 0 :
					text = "イエローカード判定が当てはまるメンバーのデータです"
					await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text, filename=send_fileName)


			else :
				text = "過去ログの音声チャンネルログイン加工済みデータを作成できませんでした"
				await interaction.message.delete()
				await Sendtool.Send_ChannelID(client=self.client, channelID=[interaction.message.channel.id], message=text)


			
			## 諸処初期化
			self.clientData.reset()

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

		self.reset()

		pass

	def reset(self):
		self.oldMode_Month_ok = False
		self.oldMode_Role_ok = False
		self.Months = 1
		
		self.roleName = ""
		self.roleID = 0
		self.guildID = 0
		self.labellist = []
		self.fileNameList = []

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		#print("test")

		self.eventButton = test_button(["過去ログ","現行ログ"], client=client ,clientData=self , config=config )
		await Sendtool.Send_Member(Data=message, message="どちらのログが欲しいですか？", filename=None,view=self.eventButton)
