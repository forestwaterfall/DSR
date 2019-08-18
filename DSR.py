# coding: UTF-8
from time import sleep
from time import time
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from user_information import login,password,LINE_token
import sys
import traceback

e=0
def main():
	try:
		number=0
		first=0
		may_p=0
		june_=0
		july_p=0
		august_p=0
		may_vacant=0
		june_vacant=0
		july_vacant=0
		august_vacant=0
		month = [0,0,0,0,0,0,0,0,0,0,0,0]

		# URL関連
		url = "http://otr.ncors.com/ncors/login.asp"

		# ヘッドレスモードの設定。
		# True => ブラウザを描写しない。
		# False => ブラウザを描写する。
		options = Options()
		options.add_argument('--headless')

		# Chromeを起動
		driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)

		# ログインページを開く
		driver.get(url)

		# ログオン処理
		# ユーザー名入力
		driver.find_element_by_name("USERID").send_keys(login)

		# パスワード入力
		driver.find_element_by_name("USERPASSWD").send_keys(password)
		driver.find_element_by_xpath("//input[@value='ログイン']").send_keys(Keys.ENTER)

		#技能予約を選択
		driver.find_element_by_xpath("//input[@value='　ＯＫ　']").send_keys(Keys.ENTER)

		while(True):
			sleep(1)
			driver.find_element_by_xpath("//input[@value='最新の情報に更新']").send_keys(Keys.ENTER)
			source = driver.page_source

			# ログイン後のトップページのソースを表示
			#print(soup)

			page_width = driver.execute_script('return document.body.scrollWidth')
			page_height = driver.execute_script('return document.body.scrollHeight')
			driver.set_window_size(page_width, page_height)
			driver.save_screenshot('screenshot.png')
			# ドライバーをクローズ
			#driver.close()
			#driver.quit()

			month_prev = month
			month = [0,0,0,0,0,0,0,0,0,0,0,0]

			days_ary = source.split('<td class="Head">0')
			#print(days_ary)
			for day in days_ary:
				if(day.count('td class')>0):
					monthnum = int(day[0:1])
				else:
					continue
				month[monthnum-1] += day.count('Free')

			if(first==1):
				print("------")
				t2=time()
				print("time = " + str(t2-t1))
				if ((t2-t1)>300):
					return 0
				for i in range(12):
					print(month[i])
					if(month[i]>month_prev[i]):
						url = "https://notify-api.line.me/api/notify"
						token = LINE_token
						headers = {"Authorization" : "Bearer "+ token}
						print("------\n*****\npost\n*****\n")
						message =  '\n%s月に予約できる時限が増えました\nhttp://otr.ncors.com/ncors/login.asp'%(i+1)
						payload = {"message" :  message}
						files = {"imageFile": open("screenshot.png", "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。

						r = requests.post(url ,headers = headers ,params=payload, files=files)
			first=1
			#raise ValueError("")
	except:
		global e
		if(e>0):
			url = "https://notify-api.line.me/api/notify"
			token = LINE_token
			print(traceback.format_exc())
			headers = {"Authorization" : "Bearer "+ token}
			message =  '\nエラーが発生しました.\n5秒後に再起動します.\n'+str(traceback.format_exc())
			payload = {"message" :  message}
			files = {"imageFile": open("screenshot.png", "rb")}
			r = requests.post(url ,headers = headers ,params=payload)
			sleep(5)
		e+=1
		if(e>9):
			url = "https://notify-api.line.me/api/notify"
			token = LINE_token
			error = str(sys.exc_info())
			headers = {"Authorization" : "Bearer "+ token}
			message =  '\nエラーが10回繰り返されたため終了します.'
			payload = {"message" :  message}
			files = {"imageFile": open("screenshot.png", "rb")}
			r = requests.post(url ,headers = headers ,params=payload)
			driver.close()
			driver.quit()
			sys.exit()
		main()
	return 0

t1 = time()
main()
