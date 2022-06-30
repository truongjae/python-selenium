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


def listCloneCookie():
	f = open("clone.txt","r+")
	data = f.readlines()
	cookies = []
	for d in data:
		cookie = d.split("|")
		cookies.append(cookie[3])
	return cookies

# def listCloneAcc():
# 	f = open("clone.txt","r+")
# 	data = f.readlines()
# 	accs = []
# 	for d in data:
# 		a = d.split("|")
# 		fa = a[2]
# 		fa = fa.replace(" ","")
# 		acc = Acc(a[0],a[1],fa,a[3])
# 		accs.append(acc)
# 	return accs

def listCloneAcc():
	f = open("clone.txt","r+")
	data = f.readlines()
	accs = []
	for d in data:
		cookie = d.split("|")
		fa = cookie[3]
		fa = fa.replace(" ","")
		acc = Acc(cookie[0],cookie[1],fa,cookie[2])
		accs.append(acc)
	return accs

def get_fb_dtsg(cookies):
	try:
		gets = requests.get("https://www.facebook.com",cookies = cookies)
		soup = BS(gets.content, "html.parser")
		gets = str(gets.text)
		gets = cut_string(gets,'["DTSGInitialData",[],{"token":"',True)
		gets = cut_string(gets,'"',False)
		return gets
	except:
		return None


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


def set_limit(cookies,fb_dtsg,account_id):
	myID = cookies['c_user']
	url = "https://m.facebook.com/api/graphql/"
	data = {
		'fb_dtsg': fb_dtsg,
		'fb_api_caller_class': 'RelayModern',
		'fb_api_req_friendly_name': 'useBillingUpdateAccountSpendLimitScreenMutation',
		'variables': '{"input":{"client_mutation_id":"8","actor_id":"'+myID+'","billable_account_payment_legacy_account_id":"'+account_id+'","new_spend_limit":{"amount":"0.1","currency":"USD"}}}',
		'doc_id': '5615899425146711'
	}
	requests.post(url,data = data, cookies = cookies)
	print("set limit thành công")


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


# arrThread = []
# for acc in listCloneAcc():
# 	t = threading.Thread(target = auto_add_card,args=(acc,))
# 	arrThread.append(t)
# 	# break
# for t in arrThread:
# 	t.start()

# arrThread = []
# for acc in listCloneAcc():
# 	auto_add_card(acc)
# 	break


def kick_camp():
	cookies = convert_cookie_to_json('sb=Hk67YuWPUIYCYB2QvuM_NUhu; datr=Hk67YoUZ0-0lZDRHFk48f5T2; dpr=1.25; m_pixel_ratio=1.25; locale=en_US; c_user=100082022655408; xs=12:5Sdb9Qsbbqco8A:2:1656506579:-1:-1; presence=C{"t3":[],"utc3":1656506745861,"v":1}; fr=02N5z1MRdHuwYKWGn.AWW4Qr47LA3LfegQJLGC-MZ2jDw.Biu04e.CM.AAA.0.0.BivEnY.AWXLUhSI9fE; usida=eyJ2ZXIiOjEsImlkIjoiQXJlOG91cjRvNDh1ciIsInRpbWUiOjE2NTY1MDgxODd9; wd=902x722')
	url = "https://business.facebook.com/api/graphql/"
	fb_dtsg = "NAcO_18gesdJywj6vVi_S4K-L1aM0B68ZTpUo14Kp1sK_JeNFZWcEHQ:12:1656506579"
	# data = {
	# 	"fb_dtsg": fb_dtsg,
	# 	"fb_api_caller_class": "RelayModern",
	# 	"fb_api_req_friendly_name": "LWICometCreateBoostedComponentMutation",
	# 	"variables": '{"input":{"creation_spec":{"ads_lwi_goal":"GET_MESSAGES","audience_option":"NCPP","auto_boost_settings_id":null,"auto_targeting_sources":null,"billing_event":"IMPRESSIONS","budget":100,"budget_type":"DAILY_BUDGET","currency":"USD","duration_in_days":2,"franchise_program_id":null,"is_automatic_goal":false,"legacy_ad_account_id":"1314321652310015","legacy_entry_point":"bizweb_ad_center_overview","logging_spec":{"reach_estimates":{"lower_estimates":269,"upper_estimates":777},"spec_history":[{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"USD"},{"budget":300,"currency":"USD"},{"budget":300,"currency":"USD"},{"budget":100,"currency":"USD"}]},"messenger_welcome_message":{"greeting":"Hi {{user_first_name}}! Please let us know how we can help you.","icebreakers":["Can I schedule a viewing?","Are there any new properties available?","Can I speak to an agent?"],"icebreakers_enabled":true},"pixel_event_type":null,"pixel_id":null,"placement_spec":{"publisher_platforms":["FACEBOOK","INSTAGRAM","MESSENGER"]},"regulated_categories":[],"regulated_category":"NONE","retargeting_enabled":false,"run_continuously":false,"saved_audience_id":null,"special_ad_category_countries":[],"start_time":null,"surface":"BIZ_WEB","targeting_spec_string":"{\"age_min\":22,\"age_max\":55,\"geo_locations\":{\"countries\":[\"SG\",\"VN\"],\"location_types\":[\"home\"]}}","adgroup_specs":[{"creative":{"degrees_of_freedom_spec":{},"instagram_actor_id":"7488085801263272","instagram_branded_content":{},"object_story_spec":{"link_data":{"call_to_action":{"type":"MESSAGE_PAGE","value":{"app_destination":"MESSENGER"}},"description":" ","link":"https://www.facebook.com/BioMix-Plus-112955148094961/","message":"Real Estate","name":"BioMix Plus","picture":"https://scontent-xsp1-1.xx.fbcdn.net/v/t39.30808-6/285324029_112956164761526_2682340800049049103_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=ca947b&_nc_ohc=AdOvnlH3e5kAX8dnzxE&_nc_ht=scontent-xsp1-1.xx&oh=00_AT-jG_JBtZjOQZWFTIIGGlam8nCpL_T_pFUiCP6oBA5ZNg&oe=62C09F9E","use_flexible_image_aspect_ratio":true},"page_id":"112955148094961"},"use_page_actor_override":null}}],"cta_data":null,"objective":"MESSAGES"},"external_dependent_ent_id":null,"flow_id":"53a4e809-a6fc-41ee-a92e-e65fd4e2ba67","manual_review_requested":false,"page_id":"112955148094961","product":"BOOSTED_CTA","target_id":"112956284761514","actor_id":"100082022655408","client_mutation_id":"1"}}',
	# 	"doc_id": "3843613959067653"
	# }




	data = {
		"fb_dtsg": fb_dtsg,
		"variables": '{"adAccountID":"1197663011036358"}',
		"doc_id": "5596350257101547"
	}
	p = requests.post(url,data=data,cookies=cookies)
	print(p.text)

	data = {
		"fb_dtsg": fb_dtsg,
		"variables": '{"input":{"creation_spec":{"ads_lwi_goal":"GET_MESSAGES","audience_option":"NCPP","auto_boost_settings_id":null,"auto_targeting_sources":null,"billing_event":"IMPRESSIONS","budget":100,"budget_type":"DAILY_BUDGET","currency":"USD","duration_in_days":2,"franchise_program_id":null,"is_automatic_goal":false,"legacy_ad_account_id":"1197663011036358","legacy_entry_point":"bizweb_ad_center_overview","logging_spec":{"reach_estimates":{"lower_estimates":180,"upper_estimates":522},"spec_history":[{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"CAD"},{"budget":300,"currency":"USD"},{"budget":300,"currency":"USD"},{"budget":300,"currency":"USD"},{"budget":300,"currency":"USD"},{"budget":100,"currency":"USD"}]},"messenger_welcome_message":{"greeting":"Hi {{user_first_name}}! Please let us know how we can help you.","icebreakers":["Can I schedule a viewing?","Are there any new properties available?","Can I speak to an agent?"],"icebreakers_enabled":true},"pixel_event_type":null,"pixel_id":null,"placement_spec":{"publisher_platforms":["FACEBOOK","INSTAGRAM","MESSENGER"]},"regulated_categories":[],"regulated_category":"NONE","retargeting_enabled":false,"run_continuously":false,"saved_audience_id":null,"special_ad_category_countries":[],"start_time":null,"surface":"BIZ_WEB","targeting_spec_string":"{\"age_min\":30,\"age_max\":55,\"geo_locations\":{\"countries\":[\"SG\",\"VN\"],\"location_types\":[\"home\"]}}","adgroup_specs":[{"creative":{"degrees_of_freedom_spec":{},"instagram_actor_id":"7488085801263272","instagram_branded_content":{},"object_story_spec":{"link_data":{"call_to_action":{"type":"MESSAGE_PAGE","value":{"app_destination":"MESSENGER"}},"description":" ","link":"https://www.facebook.com/BioMix-Plus-112955148094961/","message":"Real Estate","name":"BioMix Plus","picture":"https://scontent-xsp1-1.xx.fbcdn.net/v/t39.30808-6/285324029_112956164761526_2682340800049049103_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=ca947b&_nc_ohc=AdOvnlH3e5kAX_UXkUM&_nc_ht=scontent-xsp1-1.xx&oh=00_AT_6yM8cVPOt6YHmxkL887D_RugLZNfAKBAGQ4xx4wz-3Q&oe=62C09F9E","use_flexible_image_aspect_ratio":true},"page_id":"112955148094961"},"use_page_actor_override":null}}],"cta_data":null,"objective":"MESSAGES"},"external_dependent_ent_id":null,"flow_id":"537df82a-b235-4788-a987-a1ecc8c6236e","manual_review_requested":false,"page_id":"112955148094961","product":"BOOSTED_CTA","target_id":"112956284761514","actor_id":"100082022655408","client_mutation_id":"1"}}',
		"doc_id": "3843613959067653"
	}
	p = requests.post(url,data=data,cookies=cookies)
	print(p.text)




	data = {
		"fb_dtsg": fb_dtsg,
		"variables": '{"input":{"ad_account_id":"1197663011036358","page_id":"112955148094961","product":"BOOSTED_CTA","target_id":"112956284761514","objective":"MESSAGES"},"cta_type":"MESSAGE_PAGE"}',
		"doc_id": "2959811770810617"
	}
	p = requests.post(url,data=data,cookies=cookies)
	print(p.text)



	data = {
		"fb_dtsg": fb_dtsg,
		"variables": '{"input":{"creation_spec":{"ads_lwi_goal":"GET_MESSAGES","audience_option":"NCPP","auto_boost_settings_id":null,"auto_targeting_sources":null,"billing_event":"IMPRESSIONS","budget":100,"budget_type":"DAILY_BUDGET","currency":"USD","duration_in_days":2,"franchise_program_id":null,"is_automatic_goal":false,"legacy_ad_account_id":"612731399747425","legacy_entry_point":"bizweb_ad_center_overview","messenger_welcome_message":{"greeting":"Hi {{user_first_name}}! Please let us know how we can help you.","icebreakers":["Can I schedule a viewing?","Are there any new properties available?","Can I speak to an agent?"],"icebreakers_enabled":true},"pixel_event_type":null,"pixel_id":null,"placement_spec":{"publisher_platforms":["FACEBOOK","INSTAGRAM","MESSENGER"]},"regulated_categories":[],"regulated_category":"NONE","retargeting_enabled":false,"run_continuously":false,"saved_audience_id":null,"special_ad_category_countries":[],"start_time":null,"surface":"BIZ_WEB","targeting_spec_string":"{\"age_min\":22,\"age_max\":55,\"geo_locations\":{\"countries\":[\"SG\",\"VN\"],\"location_types\":[\"home\"]}}","adgroup_specs":[{"creative":{"degrees_of_freedom_spec":{},"instagram_actor_id":"7488085801263272","instagram_branded_content":{},"object_story_spec":{"link_data":{"call_to_action":{"type":"MESSAGE_PAGE","value":{"app_destination":"MESSENGER"}},"description":" ","link":"https://www.facebook.com/BioMix-Plus-112955148094961/","message":"Real Estate","name":"BioMix Plus","picture":"https://scontent-xsp1-1.xx.fbcdn.net/v/t39.30808-6/285324029_112956164761526_2682340800049049103_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=ca947b&_nc_ohc=AdOvnlH3e5kAX_UXkUM&_nc_ht=scontent-xsp1-1.xx&oh=00_AT_6yM8cVPOt6YHmxkL887D_RugLZNfAKBAGQ4xx4wz-3Q&oe=62C09F9E","use_flexible_image_aspect_ratio":true},"page_id":"112955148094961"},"use_page_actor_override":null}}],"cta_data":null,"objective":"MESSAGES"},"flow_id":"2dae0bb4-572a-4d76-b8e5-5b00213d839d","manual_review_requested":false,"page_id":"112955148094961","product":"BOOSTED_CTA","target_id":"112956284761514"},"scale":1.5}',
		"doc_id": "5130220923738965"
	}
	p = requests.post(url,data=data,cookies=cookies)
	print(p.text)


	data = {
		"fb_dtsg": fb_dtsg,
		"variables": '{"input":{"ad_account_id":"612731399747425","page_id":"112955148094961","product":"BOOSTED_CTA","target_id":"112956284761514","objective":"MESSAGES"},"cta_type":"MESSAGE_PAGE"}',
		"doc_id": "2959811770810617"
	}
	p = requests.post(url,data=data,cookies=cookies)
	print(p.text)




	data = {
		"fb_dtsg": fb_dtsg,
		"variables": '{"input":{"creation_spec":{"ads_lwi_goal":"GET_MESSAGES","audience_option":"NCPP","auto_boost_settings_id":null,"auto_targeting_sources":null,"billing_event":"IMPRESSIONS","budget":100,"budget_type":"DAILY_BUDGET","currency":"USD","duration_in_days":2,"franchise_program_id":null,"is_automatic_goal":false,"legacy_ad_account_id":"1197663011036358","legacy_entry_point":"bizweb_ad_center_overview","messenger_welcome_message":{"greeting":"Hi {{user_first_name}}! Please let us know how we can help you.","icebreakers":["Can I schedule a viewing?","Are there any new properties available?","Can I speak to an agent?"],"icebreakers_enabled":true},"pixel_event_type":null,"pixel_id":null,"placement_spec":{"publisher_platforms":["FACEBOOK","INSTAGRAM","MESSENGER"]},"regulated_categories":[],"regulated_category":"NONE","retargeting_enabled":false,"run_continuously":false,"saved_audience_id":null,"special_ad_category_countries":[],"start_time":null,"surface":"BIZ_WEB","targeting_spec_string":"{\"age_min\":30,\"age_max\":55,\"geo_locations\":{\"countries\":[\"SG\",\"VN\"],\"location_types\":[\"home\"]}}","adgroup_specs":[{"creative":{"degrees_of_freedom_spec":{},"instagram_actor_id":"7488085801263272","instagram_branded_content":{},"object_story_spec":{"link_data":{"call_to_action":{"type":"MESSAGE_PAGE","value":{"app_destination":"MESSENGER"}},"description":" ","link":"https://www.facebook.com/BioMix-Plus-112955148094961/","message":"Real Estate","name":"BioMix Plus","picture":"https://scontent-xsp1-1.xx.fbcdn.net/v/t39.30808-6/285324029_112956164761526_2682340800049049103_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=ca947b&_nc_ohc=AdOvnlH3e5kAX_UXkUM&_nc_ht=scontent-xsp1-1.xx&oh=00_AT_6yM8cVPOt6YHmxkL887D_RugLZNfAKBAGQ4xx4wz-3Q&oe=62C09F9E","use_flexible_image_aspect_ratio":true},"page_id":"112955148094961"},"use_page_actor_override":null}}],"cta_data":null,"objective":"MESSAGES"},"flow_id":"537df82a-b235-4788-a987-a1ecc8c6236e","manual_review_requested":false,"page_id":"112955148094961","product":"BOOSTED_CTA","target_id":"112956284761514"},"scale":1.5}',
		"doc_id": "5130220923738965"
	}
	p = requests.post(url,data=data,cookies=cookies)
	print(p.text)






kick_camp()