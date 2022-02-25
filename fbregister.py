from selenium import webdriver
from time import sleep, time
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
import time
import imaplib
import email
import traceback 

def registerFB():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.facebook.com/')
    sleep(1)

    driver.find_element(By.XPATH,"//*[text()='Create New Account']").click()
    sleep(3)
    driver.find_element(By.NAME,'firstname').send_keys('nilesh')
    driver.find_element(By.NAME,'lastname').send_keys('patil')
    driver.find_element(By.NAME,'reg_email__').send_keys('developer3.jstechno@gmail.com')
    driver.find_element(By.NAME,'reg_email_confirmation__').send_keys('developer3.jstechno@gmail.com')
    driver.find_element(By.ID,'password_step_input').send_keys('niesh@123')
    day=Select(driver.find_element(By.XPATH,'//select[@title="Day"]'))
    day.select_by_visible_text('10')
    month=Select(driver.find_element(By.NAME,'birthday_month'))
    month.select_by_visible_text('May')
    year=Select(driver.find_element(By.NAME,'birthday_year'))
    year.select_by_visible_text("2000")
    driver.find_element(By.XPATH,"//label[text()='Male']").click()
    driver.find_element(By.XPATH,"//button[text()='Sign Up']").click()
    sleep(10)   
    #driver.find_element_by_link_text("Send Email Again").click()

    # driver.find_element(By.XPATH,"//*[text()='OK']").click()

    #driver.find_element(By.NAME,'code').send_keys('12345')



# registerFB()

























def read_email_from_gmail():
    FROM_EMAIL = "developer3.jstechno@gmail.com"
    FROM_PWD = "Jstechno@123" 
    SMTP_SERVER = "imap.gmail.com" 
    SMTP_PORT = 993
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        mass=mail.fetch(str(latest_email_id),'(RFC822)')
        try:
            mass=str(mass)
            x = mass.split(' FB-')
            otp=x[1]
            otp=otp[0:6]
            print(otp)
        except Exception as e:
            print('OTP not found')
    except Exception as e:
        print('Connection failed')

# read_email_from_gmail()
