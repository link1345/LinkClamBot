
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