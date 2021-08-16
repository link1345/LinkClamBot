"""
Printに色を付けてくれるプログラム群
"""    
	
import sys
	


# その他
red_color = "\033[31m"
yellow_color = '\033[33m'
blue_color = "\033[34m"
normal_color = "\033[0m"
	
def error_print(text):
	"""
	エラー標準出力のカラー
	
	Args:
		text: 出力したい文字列
	
	return:
		None: なし
	
	"""
	
	text = red_color + "[ERROR]  " + text + normal_color
	print("{0}".format(text) , file=sys.stderr)
			
def success_print(text):
	"""
	標準出力のカラー
	
	Args:
		text: 出力したい文字列
	
	return:
		None: なし
	
	"""
	
	text = blue_color +  "[success] " + text + normal_color
	print("{0}".format(text) )
	
def warning_print(text):
	"""
	標準出力の(警告)カラー
	
	Args:
		text: 出力したい文字列
	
	return:
		None: なし
	
	"""
	
	text = yellow_color +"[WARNIG] " +  text + normal_color
	print("{0}".format(text) )