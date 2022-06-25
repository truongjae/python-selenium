import requests
from http.cookies import SimpleCookie
from time import sleep as sl
import html
from bs4 import BeautifulSoup as BS
import json
import threading
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
		check_cookie = False
		return ""

def cut_string(string,key,choice):
	index = string.find(key)
	if choice:
		string = string[index+len(key):]
	else:
		string = string[0:index]
	return string
# def get_fb_dtsg(cookies):
# 	gets = requests.get("https://m.facebook.com",cookies = cookies)
# 	soup = BS(gets.content, "html.parser")
# 	return soup.find('input', {'name': 'fb_dtsg'}).get('value')
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
		print(gets)
		return gets
		# return soup.find('input', {'name': 'fb_dtsg'}).get('value')
	except:
		return None

def followFriend(myID,idFr,fb_dtsg,cookies):
	url = "https://m.facebook.com/a/subscriptions/add?subject_id="+idFr+"&forceredirect=1&location=103&gfid=AQBhdYenT-b0l05IcQ8&refid=17"
	data = {
		'fb_dtsg': fb_dtsg,
		'jazoest' : '22025',
		'__user' : myID
	}
	requests.post(url,cookies=cookies,data=data)
def autoFollow(cookie,idFr):
	try:
		cookies = convert_cookie_to_json(cookie)
		myID = cookies['c_user']
		fb_dtsg = get_fb_dtsg(cookies)
		followFriend(myID,idFr,fb_dtsg,cookies)
		# print("xong")
	except:
		pass
# def listAccCookie():
# 	f = open("clone.txt","r+")
# 	data = f.readlines()
# 	return data

def listAccCookie():
	cookies = []
	f = open("clone.txt","r+")
	data = f.readlines()
	for d in data:
		cookie = d.split("|")[3]
		cookies.append(cookie)
	return cookies
# for cookie in listAccCookie():
# 	try:
# 		cookies = convert_cookie_to_json(cookie)
# 		myID = cookies['c_user']
# 		idFr = "100015801078321"
# 		fb_dtsg = get_fb_dtsg(cookies)
# 		followFriend(myID,idFr,fb_dtsg,cookies)
# 		print("xong")
# 	except:
# 		pass

arrThread = []
idFr = "100029031824085"
for cookie in listAccCookie():
	t = threading.Thread(target = autoFollow, args =(cookie,idFr))
	arrThread.append(t)
	# break
for t in arrThread:
	t.start()