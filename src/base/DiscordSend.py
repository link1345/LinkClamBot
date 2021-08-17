import discord

import base.EasySend as ESend
import base.ColorPrint as CPrint

def text_check(text) :
	text = text.replace("_","\_")
	text = text.replace("*","\*")
	text = text.replace("~","\~")
	text = text.replace("|","\|")
	text = text.replace("`","\`")
	text = text.replace(">","\>")
	return text

def bot_check(user: discord.Member):
	if user.bot :
		return True
	else :
		return False

		
async def Send_ChannelID(client: discord.Client, channelID: list[int], message: str, filename=None, view=None):
	"""
	指定チャンネルIDにテキストメッセージを出す。

	Args:
		channelID (int): チャンネルID
		message (str): メッセージ
	return:
		None
	"""

	for ID in channelID : 
		channel = client.get_channel( ID )
		if channel is None :
			CPrint.error_print("チャンネルが存在ぜず、送信できませんでした")
			return False
		else :
			await ESend.easy_textsend( channel, message , filename , view)
			return True

# ---------------------------------------------

async def Send_Member(Data: discord.Message, message: str, filename=None, view=None):
	"""
	discord.Messageクラスを貰った時に、そのチャンネルにメッセージを返す。

	Args:
		channelID (int): チャンネルID
		message (str): メッセージ
	return:
		None
	"""
	# Botなら、終了
	if bot_check(Data.author) :
		return
	
	await ESend.easy_textsend( Data.channel, message , filename , view)
	return True

async def Send_User(Data: discord.User, message: str, filename=None, view=None):
	"""
	discord.Messageクラスを貰った時に、そのチャンネルにメッセージを返す。

	Args:
		channelID (int): チャンネルID
		message (str): メッセージ
	return:
		None
	"""
	# Botなら、終了
	if bot_check(Data.author) :
		return
	
	ESend.easy_textsend( Data.channel, message , filename , view)
	return True