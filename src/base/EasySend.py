##############################################################################
# このファイルは、メッセージ送信を簡単にするために書いています。
#  作成 : 2019/09/21
##############################################################################
 
import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import os
import sys

import base.ColorPrint as color

async def easy_textsend( channel: discord.TextChannel, message: str , filename=None ) :
	printtext = datetime.now().strftime("%Y/%m/%d %H:%M:%S")  + " : " + message 
	print(printtext)

	# チャンネルにアクセスできない場合は、スルーします。
	if channel is not None :
		try :
			if filename is None :
				await channel.send(message)
			else :
				await channel.send(message,file=discord.File(filename))
		except discord.HTTPException as log :
			color.error_print("ERROR : メッセージの送信に失敗しました。")
			color.error_print("ERRORCORD : {0}".format(log) )
			# Sending the message failed.

		except discord.Forbidden as log :
			color.error_print("ERROR : メッセージを送る権限がありません。")
			color.error_print("ERRORCORD : {0}".format(log) )
			# You do not have the proper permissions to send the message.
			
		except discord.InvalidArgument as log :
			color.error_print("ERRORCORD : {0}".format(log) )
			# The files list is not of the appropriate size or you specified both file and files.
		except :
			color.error_print("ERROR : だめぽ {}".format(channel))