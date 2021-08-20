
import command.member_sheet.Config_Main as CSetting

import os.path

import gspread
from oauth2client.service_account import ServiceAccountCredentials 

import pandas as pd

def getGooglesheet() :

	if not os.path.exists(CSetting.credentials_filepath):
		return None

	#print("sheet load start")
 
	#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
 
	#認証情報設定
	#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
	credentials = ServiceAccountCredentials.from_json_keyfile_name(CSetting.credentials_filepath , scope)
 
	#OAuth2の資格情報を使用してGoogle APIにログインします。
	gc = gspread.authorize(credentials)
 
	#共有設定したスプレッドシートのシート1を開く
	worksheet = gc.open_by_key( CSetting.GOOGLE_SPREADSHEET_KEY ).sheet1
 
	#print("sheet load OK!")
 
	return worksheet

def getIndex_AllMember(worksheet: gspread.Spreadsheet, index_list, Flag_discord_Member):
	
	row_index = worksheet.row_values(1)
	#if not Check_ConfigList( row_index ) :
	#print(row_index)
	#print(index_list)
	if set(row_index) != set(index_list) :
		return None, None

	# ID(列)を取得
	col = worksheet.col_values(Flag_discord_Member["id"] + 1)
	col.pop(0)

	displayName_col = worksheet.col_values(Flag_discord_Member["display_name"] + 1)
	displayName_col.pop(0)

	return col , displayName_col

def getIndex(worksheet: gspread.Spreadsheet, member, index_list, Flag_discord_Member):
	# return は、 「行(member.idが当てはまる行)」 , 「列(col discordID部分)」 

	#print("member + " , member.id)
	row_index = worksheet.row_values(1)
	#if not Check_ConfigList( row_index ) :
	if set(row_index) != set(index_list) :
		return None, None

	# ID(列)を取得
	col = worksheet.col_values(Flag_discord_Member["id"] + 1)

	member_point = None
	if str(member.id) in col:
		try :
			member_point = col.index(str(member.id)) + 1
		except IndexError:
			print("名簿にいません")

	row = None
	if member_point is not None :
		row = worksheet.row_values(member_point)
	
	return row, col , member_point

def SettingIndex():
	Flag_discord_Member = {}
	Flag_discord_Member["role"] = [] # list[]
	Flag_discord_Member["id"] = None
	Flag_discord_Member["display_name"] = None
	Flag_discord_Member["name"] = None
	Flag_discord_Member["discriminator"] = None

	s_index_list = []
	for s_index in CSetting.SheetIndex :
		num = CSetting.SheetIndex.index(s_index) 
		if "text" in s_index.keys() :
			s_index_list.append( s_index["text"]["label"] )
		if "discord.Member.role" in s_index.keys() :
			s_index_list.append( s_index["discord.Member.role"]["name"] )
			Flag_discord_Member["role"].append( num )
		if "discord.Member.id" in s_index.keys() :
			s_index_list.append( s_index["discord.Member.id"] )
			Flag_discord_Member["id"] = num
		if "discord.Member.display_name" in s_index.keys() :
			s_index_list.append( s_index["discord.Member.display_name"] )
			Flag_discord_Member["display_name"] = num
		if "discord.Member.name" in s_index.keys() :
			s_index_list.append( s_index["discord.Member.name"] )
			Flag_discord_Member["name"] = num
		if "discord.Member.discriminator" in s_index.keys() :
			s_index_list.append( s_index["discord.Member.discriminator"] )
			Flag_discord_Member["discriminator"] = num
	
	return Flag_discord_Member, s_index_list