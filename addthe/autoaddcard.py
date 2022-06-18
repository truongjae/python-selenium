from selenium import webdriver
from time import sleep as sl
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup as BS

import random

import requests
from selenium.webdriver.chrome.options import Options

import threading


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


import pyautogui as pya


class Card:
	def __init__(self,code,date,ccv):
		self.code = code
		self.date = date
		self.ccv = ccv

class Acc:
	def __init__(self,tk,mk,fa,cookies):
		self.tk = tk
		self.mk = mk
		self.fa = fa
		self.cookies = cookies

def convert_cookie_to_json(string_cookie):
	temp= string_cookie.replace(" ", "")
	temp = temp.split(";")
	listKey = ["sb","datr","c_user","xs","fr"]
	listCookies = []
	for i in temp:
		key = i.split("=")[0]
		if key in listKey:
			listCookies.append(i)
	string_cookie=";".join(listCookies)
	try:
		cookie = SimpleCookie()
		cookie.load(string_cookie)
		cookies = {}
		for key, morsel in cookie.items():
		    cookies[key] = morsel.value
		return cookies
	except:
		return ""

def get2FA(fa):
	p = requests.get("https://2fa.live/tok/"+fa)
	return p.json()['token']
def listCloneCookie():
	f = open("clone.txt","r+")
	data = f.readlines()
	cookies = []
	for d in data:
		cookie = d.split("|")
		cookies.append(cookie[3])
	return cookies

def listCloneAcc():
	f = open("clone.txt","r+")
	data = f.readlines()
	accs = []
	for d in data:
		a = d.split("|")
		fa = a[2]
		fa = fa.replace(" ","")
		acc = Acc(a[0],a[1],fa,a[4])
		accs.append(acc)
	return accs

def listCard():
	f = open("card.txt","r+")
	data = f.readlines()
	cards = []
	for c in data:
		temp = c.split("|")
		date = temp[1]+temp[2][2:]
		card = Card(temp[0],date,temp[3])
		cards.append(card)
	return cards

def clickElm(driver,xpath):
	while True:
		try:
			driver.find_element_by_xpath(xpath).click()
			break
		except:
			pass

def sendKeyElm(driver,xpath,value):
	while True:
		try:
			driver.find_element_by_xpath(xpath).send_keys(value)
			break
		except:
			pass
def clearInput(driver,xpath):
	while True:
		try:
			driver.find_element_by_xpath(xpath).clear()
			break
		except:
			pass

def findElm(driver,xpath):
	count = 0
	while True:
		count+=1
		try:
			driver.find_element_by_xpath(xpath)
			return True
		except:
			pass
		if count > 8:
			return False
		sl(1)
def getAccountId(driver):
	url = driver.current_url
	acc = url.split("account_id=")
	acc_id = ""
	for i in acc[1]:
		if i=="&":
			break
		acc_id+=i
	return acc_id
def get_fb_dtsg(cookies):
	gets = requests.get("https://m.facebook.com",cookies = cookies)
	soup = BS(gets.content, "html.parser")
	return soup.find('input', {'name': 'fb_dtsg'}).get('value')
def setLimitWithApi(driver,tk,cookie):
	print("hello")
	cookies = convert_cookie_to_json(cookie)
	fb_dtsg = get_fb_dtsg(cookies)
	url = "https://m.facebook.com/api/graphql/"
	data = {
		'fb_dtsg': fb_dtsg,
		'fb_api_caller_class': 'RelayModern',
		'fb_api_req_friendly_name': 'useBillingUpdateAccountSpendLimitScreenMutation',
		'variables': '{"input":{"client_mutation_id":"8","actor_id":"'+tk+'","billable_account_payment_legacy_account_id":"'+getAccountId(driver)+'","new_spend_limit":{"amount":"0.1","currency":"USD"}}}',
		'doc_id': '5615899425146711'
	}
	requests.post(url,data = data, cookies = cookies)

def saveAccSuccess(acc):
	f = open("clonesuccess.txt","a+")
	f.write(acc.tk+"|"+acc.mk+"|"+acc.fa+"\n")

def login(acc):
	"""clone1 = listClone()[0]
	cookies = convert_cookie_to_json(clone1)
	driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=chrome_options )
	# driver.set_window_size(640, 480)
	driver.get("https://m.facebook.com")

	for cookie in cookies:
		driver.add_cookie({"name": cookie,"value": cookies[cookie]})
	# driver.refresh()
	"""
 
	driver = webdriver.Chrome(executable_path='chromedriver.exe')
	driver.set_window_size(640, 480)
	driver.get("https://m.facebook.com")
	sendKeyElm(driver,"/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/form/div[4]/div[1]/div/div/input",acc.tk)
	sendKeyElm(driver,"/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/form/div[4]/div[3]/div/div/div/div[1]/div/input",acc.mk)
	clickElm(driver,"/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/form/div[5]/div[1]/button")

	# nhap 2 fa

	sendKeyElm(driver,"/html/body/div[1]/div/div[3]/form/div/article/section/div/section[2]/div[2]/div/input",get2FA(acc.fa))

	clickElm(driver,"/html/body/div[1]/div/div[3]/form/div/article/div[1]/table/tbody/tr/td/button")

	#continue
	clickElm(driver,"/html/body/div[1]/div/div[3]/form/div/article/div[1]/table/tbody/tr/td/button")

	#check acc die
	if findElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div/form/div/div/div[2]/div[1]/div/button"):
		driver.close()

	else:

		
		addCard(driver,acc)
	
	

def addCard(driver,acc):
	global count
	driver.get("https://m.facebook.com/business_payments")

	# doi quoc gia
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/div/div/div") 
	sl(0.5)
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div") # click doi quoc gia
	sl(0.5)
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/div/div[3]/div[3]/div/div[2]/div[18]/button") # click bangladesh
	sl(1)
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div") # doi tien te
	sl(1)
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[3]/div/div[2]/div[53]/button") # us dolla
	
	# click next

	driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button").click()

	# next payment
	sl(8)
	driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button").click()
	

	
	# add card
	card = random.choice(listCard())

	sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/label/div/div[1]/div/div/input","abcdefgh")
	sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/label/div/div[1]/div/div[2]/input",card.code)
	sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/div/div/div/div/div/label/div/div[1]/div/div/input",card.date)
	sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[4]/div/div/div/div/div/label/div/div[1]/div/div/input",card.ccv)

	#click btn next
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button")


	"""
	#check add the bi die
	sl(5)
	if findElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button"):
		driver.close()


	#check the die thi nhap lai the
	if findElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[1]"):
		clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[1]/i[1]") # quay ve
		clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button") #next
		# add card
		card = random.choice(listCard())

		sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/label/div/div[1]/div/div/input","abcdefgh")
		sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/label/div/div[1]/div/div[2]/input",card.code)
		sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/div/div/div/div/div/label/div/div[1]/div/div/input",card.date)
		sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[4]/div/div/div/div/div/label/div/div[1]/div/div/input",card.ccv)

		#click btn next
		clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button")		
	"""

	# #click skip 
	# clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[4]/button")

	"""
	# set limit
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div/div[6]/div[2]/div[1]/div[1]/div/div/div[2]")

	# clearInput(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div/div[6]/div[2]/div[1]/div[1]/div/div/div[2]")

	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div/div/label/div/div[1]/div/div/input")

	
	for i in range(10):
		pya.press("backspace")
		sl(0.1)

	sendKeyElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div/div/label/div/div[1]/div/div/input","0.1")

	# click save
	clickElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/button")"""

	#set limit api
	sl(5)
	setLimitWithApi(driver,acc.tk,acc.cookies)

	saveAccSuccess(acc)

arrThread = []
for acc in listCloneAcc():
	t = threading.Thread(target = login,args=(acc,))
	arrThread.append(t)

count = 1
for t in arrThread:
	if count % 4==0:
		sl(40)
	t.start()
	count+=1



