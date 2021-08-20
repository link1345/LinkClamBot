
# 一部のデータは、全体設定の奴を流用する
import config.CommandSetting as base

# ログファイルはどこに保存するのか？
baseLogFolder = "./log/voice-log/"


# 生ログフォルダ名
JSONPATH_row = "row/"

# 最新ログファイル名
JSONPATH_now = "now.json"

# 最新加工済みログファイル名
JSONPATH_now_csv = "now.csv"

# 過去加工済みログファイル名
JSONPATH_old_csv = "old.csv"

# 加工ログフォルダ名
JSONPATH_analysis = "analysis/"


# 定期１ヵ月実行で出る加工済みログデータは、どのロールに制限して出すか？
OneMonthOutput_RoleID = [
	base.roleID["正隊員"]
]

OneMonthOutput_ChannelID = [
	base.channelID[ "幹部対応" ]
]

# 参加時間なら注意喚起
WaringTime = 0.5 # 0.5 = 30分 , 1 = 1時間

WaringMonths = 2