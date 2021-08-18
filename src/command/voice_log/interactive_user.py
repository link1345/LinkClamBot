

import discord
import base.command_base as base

import base.DiscordSend as Sendtool
import command.voice_log.chart as Chart

import command.voice_log.Config_Main as CSetting

import pandas as pd
from pprint import pprint

class command(base.command_base)  :

	def __init__(self) :
		super().__init__()
		pass

	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		
		old_month , labels , fileNameList = Chart.most_old_Month()
		print(fileNameList)

		# 参加してない月の数
		waringNum = 0

		now_filepath = CSetting.baseLogFolder + CSetting.JSONPATH_row + CSetting.JSONPATH_now
		now_timeData = await Chart.makeTimeList( client=client, Datafile_path=now_filepath, RoleList=[message.author.roles[0].id] )
		
		now_time = now_timeData.loc[message.author.id, "time"]
		
		if waringNum < CSetting.WaringTime :
			waringNum += 1
		
		await Sendtool.Send_Member(Data=message, message="今月の" + message.author.display_name + "さんのボイチャ参加時間は、**" + str( round(now_time, 2) ) + "時間**です。", filename=None)
		if now_time != 0.0 and round(now_time, 2) == 0.0 :
			await Sendtool.Send_Member(Data=message, message="**...いや、あの。表示上0時間になってますけど、短すぎなんだよなぁ…何？１秒しか参加してないの？**", filename=None)

		# 過去の参加時間
		timeData = await Chart.makeOldTimeList( client=client, MonthFileList=fileNameList , IndexLabel=labels , RoleList=[message.author.roles[0].id] )

		timeData = timeData.drop(columns=['name'])
		
		waringNum = 0
		for value in timeData.columns.values :
			if timeData.loc[message.author.id, value] >= CSetting.WaringTime :
				break
			waringNum += 1
		
		if waringNum >= CSetting.WaringMonths :
			await Sendtool.Send_Member(Data=message, message= message.author.display_name + "さん、全くVC参加してないですよね。イエローカードが" + str(waringNum) + "ヵ月出てますよ。", filename=None)
		else :
			print("safe")
