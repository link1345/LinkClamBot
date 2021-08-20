
import sys

import discord
from discord.ext import tasks

import base.command_base as base
import base.DiscordSend as Sendtool
import command.member_sheet.Config_Main as CSetting
import command.member_sheet.GoogleSheet as CSheet

import pandas as pd

from discord.ext import tasks

import copy

class command(base.command_base)  :

	def __init__(self) :
		super().__init__()

		self.talk = False
		self.talk_UserID = 0
		self.talkNum = 0

		self.stopwatch_task: tasks.Loop = None

		self.Flag_discord_Member, self.CSet_index_list = CSheet.SettingIndex()

		pass

	async def seting_message(self, message: discord.Message, member: discord.Member) :

		# シート取得
		worksheet = CSheet.getGooglesheet()
		row, col, member_point = CSheet.getIndex(worksheet, member, self.CSet_index_list, self.Flag_discord_Member)
		if len(row) < len(self.CSet_index_list) :
			emptybox = [""] * ( len(self.CSet_index_list) - len(row) )
			row = row + emptybox 

		change_after = copy.deepcopy(row)
		
		# 手動書き込み欄の個数を数える
		textindex_num = 0
		for index in CSetting.SheetIndex :
			if "text" in index.keys() :
				textindex_num += 1
		
		textbox = message.content.split("\n")

		# 設定の「手動書き込み欄の個数」より、書き込み内容の方が少なければエラー
		if len(textbox) < textindex_num :
			await Sendtool.Send_Member(Data=message, message="形式が間違っています。コマンドからやり直してください。", filename=None)
			return 

		# 記入
		textbox_num = 0
		for num in range(len(row)) :

			# auto記入欄は飛ばす
			hitflag = False
			for dis_itemKey in self.Flag_discord_Member.keys() :
				if dis_itemKey == "role" :
					for item in self.Flag_discord_Member[dis_itemKey] :
						if item == num :
							hitflag = True
							break
					if hitflag :
						break
				else :
					if self.Flag_discord_Member[dis_itemKey] == num :
						hitflag = True
						break

			if hitflag :
				continue
		
			print(change_after[num] +" = "+ textbox[textbox_num])

			# 手動記入欄
			textItem = textbox[textbox_num].split("：")
			if len(textItem) >= 2 :
				change_after[num] = textItem[1]
			textbox_num += 1
		
		change_num = 0
		for change_item in change_after :
			# このデータが変更されているか？
			#print(row[change_num] + " != " +change_item )
			if row[change_num] != change_item :
				worksheet.update_cell(member_point, change_num + 1, change_item) # 更新！
			change_num += 1
		
		await Sendtool.Send_Member(Data=message, message="名簿の設定が終わりました。\n【名簿URL】" + str( CSetting.SPREADSHEET_URL ), filename=None)
		pass


	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		#await Sendtool.Send_Member(Data=message, message="interactive test message", filename=None)

		if self.talkNum == 0 :

			self.talk = True
			self.talk_UserID  = message.author.id
			self.talkNum = 1

			text = "あなた(" + Sendtool.text_check(message.author.name) + "#" + Sendtool.text_check(message.author.discriminator) + ") さんの参加名簿情報を変更します。"
			text += "\n下記の形式で、情報を書き込んでください。(※ 3分以内に返信がないと、受付を取りやめます。)"
			#text += "\n```\nOriginID：\nVol内の呼び名：\nsteamユーザ名：\nUplay(Ubisoft)ユーザー名：\nBATTEL.NET[Battle Tag]：\nepicgamesディスプレイネーム：\nPlayStation ID：\nTwitterアカウント：\n```" )
			
			# リスト一覧
			text += "\n```"
			for num in range(len(self.CSet_index_list)) :
				
				#if num  :
				hitflag = False
				for dis_itemKey in self.Flag_discord_Member.keys() :
					if dis_itemKey == "role" :
						for item in self.Flag_discord_Member[dis_itemKey] :
							if item == num :
								hitflag = True
								break
						if hitflag :
							break
					else :
						if self.Flag_discord_Member[dis_itemKey] == num :
							hitflag = True
							break

				if hitflag :
					continue

				text += self.CSet_index_list[num].replace("\n","") + "：\n"
			text += "```"

			await Sendtool.Send_Member(Data=message, message=text, filename=None)

			async def stopwatch(self, client: discord.Client, message: discord.Message, task):
				if task.current_loop == 1 :
					self.talk = False
					self.talkNum = 0
					self.talk_UserID = 0					
					await Sendtool.Send_ChannelID(client, [message.channel.id] , "【名簿変更機能】3分以内に返信がなかったため、受付を取りやめます")
				pass
			
			if self.stopwatch_task is None :
				self.stopwatch_task = (tasks.loop(minutes=3,count=2))(stopwatch)
				self.stopwatch_task.start(self, client, message, self.stopwatch_task)
				pass

		elif self.talkNum == 1 :
			# 時間内なら、ストップウォッチを止める。
			if self.stopwatch_task.is_running() :
				self.stopwatch_task.stop()
				#print("  時間以内 -- ")

			#print( self.talk_UserID ,"==", message.author.id )
			if self.talk_UserID == message.author.id :
				#print("RUN! ")
				await self.seting_message(message, message.author)
				self.talk = False
				self.talkNum = 0
				self.talk_UserID = 0
			else :
				await Sendtool.Send_Member(Data=message, message="【名簿変更機能】他のユーザーの名簿を変更をしています。少々お待ちください。", filename=None)