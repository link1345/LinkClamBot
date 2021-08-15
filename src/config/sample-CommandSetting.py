

channelID = {
	 "正隊員対応" : "--------------------" 
}


CommandList = {}

# HELP
CommandList["HELP"] = {
	"PythonFile": "command.sample.main",
	"onMessage" :{
		"CommandText": [
			"ヘルプ",
			"、ヘルプ",
			"たすけて",
			"、たすけて",
			"Help"
			",Help",
		],
		"channelID": [ channelID[ "正隊員対応" ] ] ,
		"role": ["正隊員"],
		"ExplanatoryText": "ヘルプ **テスト文**",
	}
}
