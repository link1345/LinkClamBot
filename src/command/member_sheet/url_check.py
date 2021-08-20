
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
		pass


	async def on_message(self, config, client: discord.Client, message: discord.Message) :
		await Sendtool.Send_Member(Data=message, message="【名簿URL】" + CSetting.SPREADSHEET_URL , filename=None)
		pass