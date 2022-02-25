from selenium import webdriver
from time import sleep, time
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
#from webdriver_manager.firefox import GeckoDriverManager

# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome()

# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


gmailId='kishor869819@gmail.com'
passWord='patil@123'

driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
sleep(1)


loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
loginBox.send_keys(gmailId)

nextButton = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
nextButton[0].click()

passWordBox = driver.find_element_by_xpath('//*[@id ="password"]/div[1]/div / div[1]/input')
passWordBox.send_keys(passWord)

nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
nextButton[0].click()

print('Login Successful...!!')
