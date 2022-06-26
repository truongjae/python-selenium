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

def tag(cookies):
	url = "https://www.facebook.com/api/graphql/"
	data = {
		'fb_dtsg': 'NAcM1ImxYM_MmiAHikIANKal5lf_ZdRVfN6TNvXX1TbAHi0Z1hDavHA:39:1652095668',
		'variables': '{"displayCommentsFeedbackContext":null,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"feedLocation":"TIMELINE","feedbackSource":0,"focusCommentID":null,"groupID":null,"includeNestedComments":false,"input":{"attachments":null,"feedback_id":"ZmVlZGJhY2s6ODIxNTE1MTc4ODI2MjAy","formatting_style":null,"message":{"ranges":[{"entity":{"id":"100004768000249"},"length":8,"offset":0}],"text":"Trần Kimaa"},"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,tap_bookmark,1656193125285,404895,100029031824085","is_tracking_encrypted":true,"tracking":["AZVK0DwYw-lCVu4xFOv4Bm3pO7s8BIKO-_Y6cJ5hnMhq0BnbNe8rru4OIftv6W-KubBwIjqeUjOfLdc8oO7Xrli4EQb8g0LT0ZsQTOxm6IbMYInhA5ynHSuGHfNj7wMAM3jgiaBkejd1wfQPUW_PaoqzA7mkr_fEQbxulHJZDcV8UAlxW4tqZ8eme3hEABl2x7qBIO5oOC_KxuNqxGJaNnqlnywGGhL7J-IYCHPLIWS7SFHI-GB89GPQaR4Qn1DKwV6Y7xsSCKcStb4VrSxAyr32Kg241EuSSpgs1om3QxhCVIWtHd6nXm3FEbQVwjwdki6TpssCXmPDugJxLQvS-WQjaxuoOlPJmlCc9qWQ0d9Vq5iyaIGuNgzkDUJm-QqOxOKVXGVFwxMRIZCfqMcWovyFWJhdmIXBBD2Zn_-EDp7SJz-ARFu9JEBXWfTpauEemiEVE3GCJC9Tp4koyDE_WKgXBP76_vGHbO0jjzGID1hObALee2s9hmPsrciTRJfDpLgIkPBKkdXNUTetUZHJ8LRmgBIqixfqz-NJP9Je9LXAu7V-cSdGtkcihAUbWPwshx4NFKG2W6hhL8wNbQmvSCjwYxkEStTrz_0KG6ndSJn9z-zdPpXdqrTLynZASseSDLooqV3lQbvt5euONVc2p1Rseg_qqSBVIlQ-HWtfIua7Yf7vqbh5aFndPzD2IjMl3p0","{\"assistant_caller\":\"comet_above_composer\",\"conversation_guide_session_id\":\"8c234588-044b-4a87-b4b8-c70bcc915eb4\",\"conversation_guide_shown\":null}"],"feedback_source":"PROFILE","idempotence_token":"client:f172432a-0ce0-49db-8eb1-677210decb3a","session_id":"924a17fc-b326-43c4-ae4a-f76396493f69","actor_id":"100029031824085","client_mutation_id":"5"},"inviteShortLinkKey":null,"renderLocation":null,"scale":1,"useDefaultActor":false,"UFI2CommentsProvider_commentsKey":"ProfileCometTimelineRoute"}',
		'doc_id': '7879146618827230'
	}
	p = requests.post(url,data = data,cookies = cookies)
def like(cookies):
	cookies = convert_cookie_to_json(cookies)
	myID = cookies['c_user']
	url = "https://www.facebook.com/api/graphql/"
	fb_dtsg = get_fb_dtsg(cookies)
	print(fb_dtsg)
	data = {
		'fb_dtsg': fb_dtsg,
		'doc_id': '5987089471325144',
		'variables': '{"input":{"attribution_id_v2":"CometPhotoRoot.react,comet.mediaviewer.photo,via_cold_start,1656193686093,164384,","feedback_id":"ZmVlZGJhY2s6MTIyOTEwOTUyMDk1OTA3Mg==","feedback_reaction_id":"1678524932434102","feedback_source":"MEDIA_VIEWER","is_tracking_encrypted":true,"tracking":[],"session_id":"cdc5e2f3-d18d-422a-85df-e82eff058c62","actor_id":"'+myID+'","client_mutation_id":"5"},"useDefaultActor":false,"scale":1}'
	}
	requests.post(url,data = data, cookies = cookies)

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

#follow
# arrThread = []
# idFr = "100029031824085"
# for cookie in listAccCookie():
# 	t = threading.Thread(target = autoFollow, args =(cookie,idFr))
# 	arrThread.append(t)
# 	# break
# for t in arrThread:
# 	t.start()

#like


arrThread = []
for cookie in listAccCookie():
	t = threading.Thread(target = like, args =(cookie,))
	arrThread.append(t)
	# break
for t in arrThread:
	t.start()
