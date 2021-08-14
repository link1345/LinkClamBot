import discord

from functools import singledispatch

import base.EasySend as ESend

def text_check(text) :
	text = text.replace("_","\_")
	text = text.replace("*","\*")
	text = text.replace("~","\~")
	text = text.replace("|","\|")
	text = text.replace("`","\`")
	text = text.replace(">","\>")
	return text


async def Send_channel(channelID: int, member: discord.Member , message: str, filename=None):
	"""
	指定チャンネルIDにテキストメッセージを出す。

	Args:
		channelID (int): チャンネルID
		message (str): メッセージ
	return:
		None
	"""

	if member.bot :
		return

	channel = self.client.get_channel( channelID )
	if channel is None :
		return False
	else :
		ESend.easy_textsend( channel, message , filename )
		return True

# ---------------------------------------------

@singledispatch
async def Send(Data: discord.Message, message: str, filename=None):
	"""
	discord.Messageクラスを貰った時に、そのチャンネルにメッセージを返す。

	Args:
		channelID (int): チャンネルID
		message (str): メッセージ
	return:
		None
	"""
	# Botなら、終了
	if Data.author.bot :
		return False
	
	await ESend.easy_textsend( Data.channel, message , filename )
	return True

@Send.register
async def _(Data: discord.User, message: str, filename=None):
	"""
	discord.Messageクラスを貰った時に、そのチャンネルにメッセージを返す。

	Args:
		channelID (int): チャンネルID
		message (str): メッセージ
	return:
		None
	"""
	# Botなら、終了
	if Data.author.bot :
		print("test out!")
		return False
	
	ESend.easy_textsend( Data.channel, message , filename )
	return True