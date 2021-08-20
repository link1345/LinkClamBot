
# 一部のデータは、全体設定の奴を流用する
import config.CommandSetting as base

# シートのID
GOOGLE_SPREADSHEET_KEY=''
SPREADSHEET_URL= "https://docs.google.com/spreadsheets/------"

# シートの認証ファイル(json)
credentials_filepath="./command/member_sheet/aaaaaaaaaaaaaaaaaaa.json"


# シートを上位権限で変更できるロールIDは？
SheetAdminRoleID = [ base.roleID["幹部"] ]

# シート自動更新機能動作時、不具合があったときのエラーログ出力チャンネルは？
AutoEvent_ERRORMessage_channelID =  [ base.channelID["幹部対応"] ]

### 項目
# discord.Member.id : int #必須
# discord.Member.display_name : str
# discord.Member.name : str
# discord.Member.discriminator : str
# discord.Member.role : int ※ 複数受け付けの場合は、or判定になる

# text : str [**手動登録**]
# => active : 本人変更可能 と 上位権限者(SheetAdminRoleID) 操作可能
# => invalid : 特定ロール所有者以外 操作不可能欄
SheetIndex = [
	{
		"text" : {
			"label": "test",
			"flag" : "invalid",
		},
	},
	{
		"text" : {
			"label": "呼び名",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "OriginID",
			"flag" : "active",
		},
	},
	{"discord.Member.role" : { "name": "役職:幹部", "roles": [base.roleID["幹部"]] } },
	{"discord.Member.role" : { "name": "役職:正隊員", "roles": [base.roleID["正隊員"]] } },
	{"discord.Member.role" : { "name": "役職:仮入隊", "roles": [base.roleID["仮入隊"]] } },
	{"discord.Member.id" : "Discord ID" }, # 必須
	{"discord.Member.display_name" : "Discord\nDisplayName" },
	{"discord.Member.name" : "Discord\nName" },
	#{"discord.Member.discriminator" : "Discord\ndiscriminator" },
	{
		"text" : {
			"label": "steam\nユーザー名",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "Uplay(Ubisoft)\nユーザー名",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "BATTEL.NET\nBattleTag",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "epicgames\nディスプレイネーム",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "XBOX\nゲーマータグ",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "PlayStation ID",
			"flag" : "active",
		},
	},
	{
		"text" : {
			"label": "Twitter\nアカウントURL",
			"flag" : "active",
		},
	},
]