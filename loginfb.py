from selenium import webdriver
from time import sleep as sl
import pyautogui as pya
import pickle
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.maximize_window()
driver.get("https://m.facebook.com")

def saveAcc(user,pw):
	with open("acc.txt","a+") as f:
		f.write(user+"-"+pw+"\n")
def login():
	try:
		driver.find_element_by_id('m_login_email').send_keys("trangnguyen191002@gmail.com")
		driver.find_element_by_id('m_login_password').send_keys("vemedia1505")
		driver.find_element_by_id('login_password_step_element').click()
		print(driver.get_cookies())
	except:
		print("error")
	# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
login()

#404644