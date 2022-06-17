from selenium import webdriver
from time import sleep as sl
from http.cookies import SimpleCookie
import threading
list_cookie = ['datr=44OOYmQmIlQBWggDuBUj6YD3; fr=0uaFzvwAaXMM5hP8e.AWWrgI8aR97I_sdqav_7OrSPl6Y.BijoRJ.nv.AAA.0.0.BijoSh.AWX8MzIw6LY; sb=oYSOYvYSbUKPMgeoptdvEwT9; c_user=100081787684507; xs=14%3AReNwLipdnvQFxA%3A2%3A1653507238%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=5YWOYt11JKey98PsPjIDB7Gt; fr=0XyXI1JeOuKcIY81t.AWWt7fJ2jugpbuLFNXfyZPm-loI.BijoZL.r2.AAA.0.0.Bijoe5.AWUcJugoHMg; sb=DoaOYrvcri80GzsbnSr-xiXf; c_user=100081193347137; xs=48%3AjXnS0qmbbqb7Mw%3A2%3A1653508032%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=aYiOYqqAILVoDRDZC_BOTLy5; fr=0U20wqmZxGo07SSok.AWUOSGNhR2Zcq9Xev7sRCJFPR60.Bijoir.Or.AAA.0.0.BijomJ.AWUunJp2kEM; sb=iYmOYuUmlUHeh8m5_HKC0EZs; c_user=100081302931207; xs=44%3AutUM25qWe4CZaQ%3A2%3A1653508494%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=5oWOYglR_qUzf12-3XJnRM3Z; fr=0XSz2vVKDN4YQApkO.AWXlYpf7ZTZWSm4wQtoFXPUSJC4.BijoYn.tL.AAA.0.0.Bijoe4.AWVe04DejcQ; sb=uIeOYurkSD3y8BMvNFgCZIg4; c_user=100081797074160; xs=9%3AJIet7pqsmt-VIQ%3A2%3A1653508029%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=2oWOYr-BwR-5137IC26R_5h5; fr=0VdUFOi3GCq98pQrm.AWVbtFVx-wJFVM8mIfJ9YZ-WIYE.BijoYg.Wr.AAA.0.0.BijoYl.AWUwrTjfRR4; sb=JYaOYgWh8TieTCxV2sRtHQIa; c_user=100081173457891; xs=33%3A4um2VsoOulxFPA%3A2%3A1653507639%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=M3aOYiJN336FnnOLnDSb45Pu; fr=0wmX1kjxYzfUl8BNi.AWUfpCf7tT21utB4JNuWAfaOsOk.BijnZ6.A0.AAA.0.0.Bijnaj.AWXn-pDnCds; sb=o3aOYp1BTncUrBYXKTTycuGx; c_user=100081811983330; xs=24%3A8U85Z_zxjQF7Jw%3A2%3A1653503656%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=boiOYmSEytWlWWwW4ygSIJ42; fr=0EtjBYSVW723GxMyD.AWXmrkVIKzXRz4paF2Jhcn8wOuI.Bijoit.N0.AAA.0.0.Bijooh.AWUrb-oHrow; sb=IYqOYkwsq_wha4_6TOQGaA1h; c_user=100081669518417; xs=42%3AnUXMv9EvRKgvGQ%3A2%3A1653508651%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=bYiOYtV88C3E4urKPmicq4pW; fr=017mpCezUDHrErMLG.AWVFqU9NVY7C-LWYcbk3ZwA5WeQ.Bijois.7Q.AAA.0.0.BijooJ.AWVXBX9UwWE; sb=CYqOYleXvAyIuo2Ht9IWVENi; c_user=100081590471588; xs=12%3AjcB1oin5Y3ULRA%3A2%3A1653508622%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=aIiOYihmJee8zY3ujG2V7Fe7; fr=0QDgfWtIiBROKLq03.AWUozEMw58llbin4ed75IO2J9_8.Bijoj2.lA.AAA.0.0.BijomB.AWXfX4KueYg; sb=gYmOYtbIOWZse-hOrKnsoGT-; c_user=100081490605704; xs=38%3A8eIZ71KHKdwqhw%3A2%3A1653508488%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=aIiOYn4mp3eXMyiit5TviZ8d; fr=0i0JHN3EScn7dRwIZ.AWW-CwcZ-UONWjzM2eM6scmFXQM.Bijoj1.o2.AAA.0.0.BijomU.AWWVQbs24fA; sb=lImOYmng2gqJUy64lOsyL7N9; c_user=100081269273852; xs=27%3ASy8I4Ri3gooHiw%3A2%3A1653508505%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=3YWOYoY14rWGBd63jPq0qI-x; fr=0fiRRxChH0AkCaJ94.AWWhn3dHUVYr9rEc2ACUU6uMMwc.BijoYZ.74.AAA.0.0.BijoY5.AWXCHhOX0WA; sb=OYaOYmIpafrUurh5FiwQdx_E; c_user=100081514005019; xs=3%3ABOYnTgFhoCi7Ow%3A2%3A1653507645%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=boiOYsGYalFS6MKcT2MXllLO; fr=04VEqhxwYLJ164SFu.AWXGllqd-B3yBBcxLxgIofsveZg.Bijoiu.yE.AAA.0.0.Bijoog.AWW7WAUrwe0; sb=IIqOYoIhXqMqps0TCWCqIecF; c_user=100081179787572; xs=15%3AWzk8PE32avQQ8g%3A2%3A1653508645%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=bYiOYuwtgcMednwBk-ARN9fd; fr=0vgRpxmNrqOo2vqMI.AWVxw4NYUY6iAT-dGJAoYBjzTwE.Bijoit.Bf.AAA.0.0.BijooQ.AWUByllIewU; sb=EIqOYhVadyXEKLbpMHlIcRnY; c_user=100081835952092; xs=34%3Ad3MaLIapiEiKLw%3A2%3A1653508630%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=44WOYmCHYMsHxOJ5dfTArRtR; fr=0fmpOVa6J1pIaGbcf.AWVDYcPUMEmLH3Qdom5ta3849bw.BijoYx.q2.AAA.0.0.BijodV.AWUtANj9YcE; sb=VYeOYpzsh60j4t3fZOmkzy-5; c_user=100081789364106; xs=32%3Ae-Vbg3YfcpkOZg%3A2%3A1653507932%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=3YWOYtNUxC6uqQp9ovYzrUae; fr=0PIGXe32e4CkYQ7By.AWWQ57xkHBkizfFihWfPpEDInhw.BijoYa.BF.AAA.0.0.BijoZR.AWW-ntnWLl8; sb=UYaOYsz3Pj3PYiZaejaY7NM2; c_user=100081653049259; xs=35%3A8jjol5A0NPmMIA%3A2%3A1653507670%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=4oWOYmo60DUsHFFwtTj09Iyo; fr=0F8FzLoDOh08vrWZJ.AWXbZXDqhXda4dQTFfjTGGDzxt8.BijoYm.FZ.AAA.0.0.BijodU.AWVkBO871CU; sb=VIeOYjjqOayZCF_pltdjcea2; c_user=100081812193461; xs=19%3AZ3_L9jITEUEAZA%3A2%3A1653507932%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=aoiOYjH6gWzK6901ww1BipWc; fr=0o9rLVInKAFzwwV3s.AWVfc-q81G5RFCtl4QmCi2j_r7c.Bijoir.kn.AAA.0.0.BijomI.AWXkCuV8A6s; sb=iImOYh_-KM6f9au463YdqP4T; c_user=100081248454972; xs=5%3AV8FnTUqVWpiWyw%3A2%3A1653508493%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=bYiOYnHjlYaRq66zQWyleC2l; fr=0d7e6kdqHGKhONrOz.AWVkzJ7rxZ05KX_e6eIv4dDROYc.Bijoit.xA.AAA.0.0.Bijoof.AWVvo24tVxs; sb=H4qOYmVQKURp4skGBcW6UJJ6; c_user=100081272363723; xs=44%3Av4Yb-wfrYCGoUQ%3A2%3A1653508644%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=3IWOYlLFa-fREqlIj3Ibb9FV; fr=0OoeUQZC2rR6potVe.AWXKan7oIFcWN_tsaNFmoQ8ouwk.BijoYd.q0.AAA.0.0.BijoZQ.AWXyfh4HxY8; sb=UIaOYh57T62vJVXfEMkwnx2s; c_user=100081277673498; xs=24%3Adrq6-tPohRtnYA%3A2%3A1653507675%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080', 'datr=bIiOYuRgUJhHopuMfSSTzekK; fr=0OYQzZ2Qrbmovmvx3.AWVroNFdWLG7FC1g5enZ6ojr0CM.Bijois.SX.AAA.0.0.BijooI.AWXurf1ByD8; sb=CIqOYoFQd90f6Y4OENeeQgfF; c_user=100081306321897; xs=34%3AhHsrNcamflT6Vg%3A2%3A1653508629%3A-1%3A-1; m_pixel_ratio=0.5; wd=1920x1080']

# list_cookie = list_cookie.split("\n")
# arr = []
# for cookie in list_cookie:
# 	cookie = cookie.split("|")
# 	for c in cookie:
# 		if "datr" in c:
# 			arr.append(c)

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

def report_group(cc):
	cookies = convert_cookie_to_json(cc)
	driver = webdriver.Chrome(executable_path='chromedriver.exe')
	driver.set_window_size(640, 480)
	driver.get("https://m.facebook.com/groups/773800139385628")

	for cookie in cookies:
		driver.add_cookie({"name": cookie,"value": cookies[cookie]})
	driver.refresh()
	sl(5)

	dau3cham = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/a/div/div/div[2]/div/i[1]")
	dau3cham.click()
	sl(10)
	report_group = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/div[3]/div[2]/div")
	report_group.click()

	sl(5)
	report_spam = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div[7]")
	report_spam.click()

	sl(5)

	button_report = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div[2]/div[3]/div/button")
	button_report.click()

	sl(5)
	
arrThread = []
for i in list_cookie:
	t = threading.Thread(target=report_group,args=(i,))
	arrThread.append(t)

for i in arrThread:
	i.start()