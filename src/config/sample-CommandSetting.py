
## -----------------
# ID setting
# **** Configure to your environment. ****

channelID = {
	"正隊員対応" : 0 ,
	"幹部対応"   : 0,
}

roleID = {
	"正隊員": 0,
	"幹部" : 0,
	"仮入隊" : 0,
	"everyone": 0,
}

## -----------------
## ----- base

CommandList = {}

# MODULE RELOAD
CommandList["RELOAD"] = {
	"PythonFile": "command.module-reload.main",
	"onMessage" :{
		"CommandText": [
			",reload",
		],
		"channelID": [ channelID[ "幹部対応" ] ] ,
		"role": [ roleID["幹部"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

# HELP
CommandList["HELP"] = {
	"PythonFile": "command.sample.main",
	"onMessage" :{
		"CommandText": [
			"ヘルプ",
			"、ヘルプ",
			"たすけて",
			"、たすけて",
			"Help",
			",Help",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

## -----------------
## ----- voice history

CommandList["VOICE_LOG"] = {
	"PythonFile": "command.voice_log.main",
	"Add_Module": [
		"command.voice_log.chart",
		"command.voice_log.Config_Main",
	],
	"on_voice_state_update" :{
	},
	#"onMessage" :{
	#	"CommandText": [
	#		"、ログ",
	#	],
	#	"ExplanatoryText": "ログ出力",
	#},
	"on_task":{
		"voice_outputlog":{
			"hours":0.0,
			"minutes":10.0,
			"seconds":0.0,
			"message-channelID": [ channelID[ "正隊員対応" ] ],
		}
	}
}

CommandList["INTERACITVE_VOICE_LOG"] = {
	"PythonFile": "command.voice_log.interactive",
	"onMessage" :{
		"CommandText": [
			"、ログ取得したい",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

CommandList["USER_INTERACITVE_VOICE_LOG"] = {
	"PythonFile": "command.voice_log.interactive_user",
	"onMessage" :{
		"CommandText": [
			"、自分の参加時間は？",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

## -----------------
## ----- member Sheet

CommandList["MEMBER_SHEET_AUTO"] = {
	"PythonFile": "command.member_sheet.auto",
	"Add_Module": [
		"command.member_sheet.Config_Main",
		"command.member_sheet.GoogleSheet"
	],
	"on_member_update":{
		"role": [ roleID["正隊員"],roleID["仮入隊"],roleID["幹部"] ],
	},
	"on_member_remove":{
		"role": [ roleID["正隊員"],roleID["仮入隊"],roleID["幹部"] ],
	},
	"on_user_update":{
		"role": [ roleID["正隊員"],roleID["仮入隊"],roleID["幹部"] ],
	},
	"on_member_join":{
		"role": [ roleID["everyone"] ],
	},
}

CommandList["MEMBER_SHEET_INTERACITVE"] = {
	"PythonFile": "command.member_sheet.interactive_user",
	"onMessage" :{
		"CommandText": [
			"、自分の名簿情報を変更する",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

CommandList["MEMBER_SHEET_INTERACITVE_URL"] = {
	"PythonFile": "command.member_sheet.url_check",
	"onMessage" :{
		"CommandText": [
			"、名簿の置き場所を教えて",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

CommandList["MEMBER_SHEET_INTERACITVE_ADMIN"] = {
	"PythonFile": "command.member_sheet.interactive_admin",
	"onMessage" :{
		"CommandText": [
			"、上位権限で名簿情報を変更する",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}

CommandList["MEMBER_SHEET_CONSISTENCY_ADMIN"] = {
	"PythonFile": "command.member_sheet.check_consistency",
	"onMessage" :{
		"CommandText": [
			"、名簿整合性チェック",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": [ roleID["正隊員"] ],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}


## -----------------
## ----- ERROR
error_path = "log/error.log"