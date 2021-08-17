
from datetime import datetime, timedelta

def check( item:str, time:str):
	## 本番用
	now = datetime.now().strftime(item)
	##   1日の0時に名前を変えて保存する。
	return bool( now == item )