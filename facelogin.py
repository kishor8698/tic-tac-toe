from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome()

browser.get("https://www.facebook.com/login/")
username = browser.find_element_by_id('devloper3.jstechno@gmail.com')
password = browser.find_element_by_id('Zxcv@123')
submit = browser.find_element_by_id('u_0_2')
username.send_keys('nileshdeveloper')
password.send_keys('Zxcv@123')

submit.click()
