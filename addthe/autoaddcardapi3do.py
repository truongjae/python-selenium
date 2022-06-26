from selenium import webdriver
from time import sleep as sl
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup as BS
from requests import session
import random

import requests
from selenium.webdriver.chrome.options import Options
import mechanize

import threading


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

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

def getCookieFromDriver(driver):
	keyCookies = ["sb","datr","c_user","xs","fr"]
	string_cookie = ""
	for key in keyCookies:
		string_cookie+= key+"="+driver.get_cookie(key)['value']+";"
	return string_cookie

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
		acc = Acc(a[0],a[1],fa,a[3])
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
	# try:
	# 	gets = requests.get("https://m.facebook.com/home.php?ref=wizard&_rdr",cookies = cookies)
	# 	soup = BS(gets.content, "html.parser")
	# 	return soup.find('input', {'name': 'fb_dtsg'}).get('value')
	# except:
	# 	return None
	try:
		gets = requests.get("https://www.facebook.com",cookies = cookies)
		soup = BS(gets.content, "html.parser")
		gets = str(gets.text)
		gets = cut_string(gets,'["DTSGInitialData",[],{"token":"',True)
		gets = cut_string(gets,'"',False)
		return gets
		# return soup.find('input', {'name': 'fb_dtsg'}).get('value')
	except:
		return None
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

# def login(acc):
# 	driver = webdriver.Chrome(executable_path='chromedriver.exe')
# 	driver.set_window_size(640, 480)
# 	driver.get("https://m.facebook.com")
# 	sendKeyElm(driver,"/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/form/div[4]/div[1]/div/div/input",acc.tk)
# 	sendKeyElm(driver,"/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/form/div[4]/div[3]/div/div/div/div[1]/div/input",acc.mk)
# 	clickElm(driver,"/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/form/div[5]/div[1]/button")

# 	# nhap 2 fa

# 	sendKeyElm(driver,"/html/body/div[1]/div/div[3]/form/div/article/section/div/section[2]/div[2]/div/input",get2FA(acc.fa))

# 	clickElm(driver,"/html/body/div[1]/div/div[3]/form/div/article/div[1]/table/tbody/tr/td/button")

# 	#continue
# 	clickElm(driver,"/html/body/div[1]/div/div[3]/form/div/article/div[1]/table/tbody/tr/td/button")

# 	#check acc die
# 	if findElm(driver,"/html/body/div[1]/div/div[4]/div/div[1]/div/div/form/div/div/div[2]/div[1]/div/button"):
# 		driver.close()
# 	else:
# 		addCard(driver,acc)


def cut_string(string,key,choice):
	index = string.find(key)
	if choice:
		string = string[index+len(key):]
	else:
		string = string[0:index]
	return string

def get_account_id(cookies):
	url = "https://www.facebook.com/business_payments"
	p = requests.get(url,cookies = cookies)
	data = str(p.text)
	data = cut_string(data,'"props":{"account_id":"',True)
	data = cut_string(data,'"',False)
	return data

def set_country_and_currentcy(cookies,fb_dtsg,account_id):
	url = "https://m.facebook.com/api/graphql/"
	myID = cookies['c_user']
	data = {
		'fb_dtsg': fb_dtsg,
		'variables': '{"input":{"client_mutation_id":"3","actor_id":"'+myID+'","billable_account_payment_legacy_account_id":"'+account_id+'","currency":"TWD","logging_data":{"logging_counter":13,"logging_id":"113367954"},"tax":{"business_address":{"city":"","country_code":"TW","state":"","street1":"","street2":"","zip":""},"business_name":"","is_personal_use":false,"second_tax_id":"","second_tax_id_type":null,"tax_exempt":false,"tax_id":"","tax_id_type":"NONE"},"timezone":"Asia/Jakarta"}}',
		'doc_id': '5428097817221702'
	}
	requests.post(url,data = data, cookies = cookies)
	print("đổi tiền thành công")
def set_country_and_currentcy_lol(cookies,fb_dtsg,account_id):
	url = "https://m.facebook.com/api/graphql/"
	myID = cookies['c_user']
	data = {
		'fb_dtsg': fb_dtsg,
		'variables': '{"input":{"client_mutation_id":"3","actor_id":"'+myID+'","billable_account_payment_legacy_account_id":"'+account_id+'","currency":"TWD","logging_data":{"logging_counter":13,"logging_id":"526291686"},"tax":{"business_address":{"city":"","country_code":"TW","state":"","street1":"","street2":"","zip":""},"business_name":"","is_personal_use":false,"tax_id":"1234567891025"},"timezone":"Asia/Jakarta"}}',
		'doc_id': '5428097817221702'
	}
	requests.post(url,data = data, cookies = cookies)
	print("đổi tiền thành công")
def list_card():
	f = open("card.txt","r+")
	data = f.readlines()
	cards = []
	for c in data:
		temp = c.split("|")
		date = temp[1]+"|"+temp[2]
		card = Card(temp[0],date,temp[3])
		cards.append(card)
	return cards

def add_card(cookies,fb_dtsg,account_id,card):
	myID = cookies['c_user']
	url = "https://m.secure.facebook.com/ajax/payment/token_proxy.php?tpe=%2Fapi%2Fgraphql%2F"
	card_first_6 = card.code[:6]
	card_last_4 = card.code[len(card.code)-4:]
	date = card.date.split("|")
	month = date[0]
	year = date[1]

	if int(month) < 10:
		month = month[1]

	data = {
		'fb_dtsg': fb_dtsg,
		'variables': '{"input":{"client_mutation_id":"6","actor_id":"'+myID+'","billing_address":{"country_code":"BD"},"billing_logging_data":{"logging_counter":28,"logging_id":"3221251053"},"cardholder_name":"abcde","credit_card_first_6":{"sensitive_string_value":"'+card_first_6+'"},"credit_card_last_4":{"sensitive_string_value":"'+card_last_4+'"},"credit_card_number":{"sensitive_string_value":"'+card.code+'"},"csc":{"sensitive_string_value":"'+card.ccv+'"},"expiry_month":"'+month+'","expiry_year":"'+year+'","payment_account_id":"'+account_id+'","payment_type":"MOR_ADS_INVOICE","unified_payments_api":true}}',
		'doc_id': '4126726757375265'
	}
	requests.post(url,data = data, cookies = cookies)
	print("add thẻ thành công")
def set_limit(cookies,fb_dtsg,account_id):
	myID = cookies['c_user']
	url = "https://m.facebook.com/api/graphql/"
	data = {
		'fb_dtsg': fb_dtsg,
		'fb_api_caller_class': 'RelayModern',
		'fb_api_req_friendly_name': 'useBillingUpdateAccountSpendLimitScreenMutation',
		'variables': '{"input":{"client_mutation_id":"8","actor_id":"'+myID+'","billable_account_payment_legacy_account_id":"'+account_id+'","new_spend_limit":{"amount":"1","currency":"TWD"}}}',
		'doc_id': '5615899425146711'
	}
	requests.post(url,data = data, cookies = cookies)
	print("set limit thành công")
def approve(cookies,fb_dtsg,account_id):
	myID = cookies['c_user']
	url = "https://m.facebook.com/api/graphql/"
	data = {
		'fb_dtsg': fb_dtsg,
		'fb_api_caller_class': 'RelayModern',
		'fb_api_req_friendly_name': 'useBillingPreauthPermitMutation',
		'variables': '{"input":{"client_mutation_id":"1","actor_id":"'+myID+'","billable_account_payment_legacy_account_id":"'+account_id+'","entry_point":"BILLING_2_0"}}',
		'doc_id': '3514448948659909'
	}
	requests.post(url,data = data, cookies = cookies)
def set_tax(cookies,fb_dtsg,account_id):
	myID = cookies['c_user']
	url = "https://m.facebook.com/api/graphql/"
	data = {
		'fb_dtsg': fb_dtsg,
		'fb_api_caller_class': 'RelayModern',
		'fb_api_req_friendly_name': 'BillingAccountInformationUtilsUpdateAccountMutation',
		'variables': '{"input":{"client_mutation_id":"2","actor_id":"'+myID+'","billable_account_payment_legacy_account_id":"'+account_id+'","currency":null,"logging_data":{"logging_counter":9,"logging_id":"3577491254"},"tax":{"business_address":{"city":"abcdefgh","country_code":"US","state":"AK","street1":"abcdefgh","street2":"abcdefgh","zip":"10000"},"business_name":"abcdefgh","is_personal_use":false},"timezone":null}}',
		'doc_id': '5428097817221702'
	}
	requests.post(url,data = data, cookies = cookies)
	print("set tax thành công")
def auto_add_card(acc):
	# cookies = convert_cookie_to_json(acc.cookies)
	# fb_dtsg = get_fb_dtsg(cookies)
	# sl(5)
	# account_id = get_account_id(cookies)
	# sl(5)
	# set_country_and_currentcy(cookies,fb_dtsg,account_id)
	# sl(5)
	# card = random.choice(list_card())
	# add_card(cookies,fb_dtsg,account_id,card)
	# sl(3)
	# set_limit(cookies,fb_dtsg,account_id)
	# # approve(cookies,fb_dtsg,account_id)
	# saveAccSuccess(acc)


	cookies = convert_cookie_to_json(acc.cookies)
	fb_dtsg = get_fb_dtsg(cookies)
	print(fb_dtsg)
	account_id = get_account_id(cookies)
	print(account_id)
	set_country_and_currentcy_lol(cookies,fb_dtsg,account_id)
	card = random.choice(list_card())
	add_card(cookies,fb_dtsg,account_id,card)
	set_limit(cookies,fb_dtsg,account_id)
	# set_tax(cookies,fb_dtsg,account_id)
	saveAccSuccess(acc)


def login(email,pw,fa):
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	cookies = mechanize.CookieJar()
	browser.set_cookiejar(cookies)
	browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
	browser.set_handle_refresh(False)
	url = 'http://m.facebook.com/login.php'
	browser.open(url)
	browser.select_form(nr = 0)
	browser.form['email'] = email
	browser.form['pass'] = pw
	response = browser.submit()

	browser.open("https://m.facebook.com/checkpoint/?__req=7")
	browser.select_form(nr = 0)
	browser.form['approvals_code'] = get2FA(fa)
	response = browser.submit()

	for i in range(3):
		try:
			browser.open("https://m.facebook.com/login/checkpoint/")
			browser.select_form(nr = 0)
			response = browser.submit()
		except:
			pass

	# print(response.read())

	return str(browser._ua_handlers['_cookies'].cookiejar)
	


def getCookie(listCookies):
	listCookies = listCookies.split("CookieJar")
	listCookies = listCookies[1]
	listCookies = listCookies[1:len(listCookies)-2]
	listCookies = " "+listCookies
	listCookies = listCookies.split(",")
	result = ""
	for cookie in listCookies:
		temp = cookie.split(" ")
		if temp[2]!="noscript=1":
			result+=temp[2]+";"
	result = result[0:len(result)-1]
	return result

# print(getCookie(login("100082567838909","melvindgvmclaughlin615","Q3OIYANFSR5CRRU2TC3YEXLD7LACQ2JN")))


arrThread = []
for acc in listCloneAcc():
	t = threading.Thread(target = auto_add_card,args=(acc,))
	arrThread.append(t)
	# break
for t in arrThread:
	t.start()
