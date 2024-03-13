from selenium import webdriver
import requests
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import traceback

url = "https://www.pap.pl/"
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
try:
	driver.get(url)
	driver.find_element("xpath", "//div[contains(@class, 'ok closeButton')]").click()
	driver.maximize_window()
	driver.find_element("xpath", "/html/body/div/header/nav/div/div[2]/ul[2]/li[3]/a").click()
	driver.find_element("xpath", "/html/body/div/header/nav/div/div[2]/nav/ul/li[3]/a").click()
	elements = driver.find_elements("class name", "title")
	titles = []
	for el in elements:
		print(el.text)
		titles.append(el.text)
	images = driver.find_elements("tag name", "img")
	for img in images:
		src = img.get_attribute("src")
		response = requests.get(src)
		pos = len(src) - src[::-1].index('/')
		filename = "images/"+src[pos:].split("?")[0]
		with open(filename, 'wb') as f:
			print(f"Saving {src} to {filename}...")
			f.write(response.content)
	driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
	driver.find_element("xpath", "//a[contains(@title, 'Go to last page')]").click()
	pg_n = driver.find_element("xpath", "//li[contains(@class, 'pager__item is-active active')]")
	print(pg_n.text)
	driver.close()
except:
	driver.close()
	traceback.print_exc()
