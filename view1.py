from datetime import datetime
from typing import List
from django.shortcuts import render,redirect
from roi_calculation import ethereum_price
from roi_calculation import tawncoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pyasn1.type.univ import Null
from df2gspread import df2gspread as d2g# The path of client_secret json file that you have downloaded
import gspread
import gspread_dataframe as gd
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from selenium.webdriver.common.by import By
from django.conf import settings
from django.core.mail import send_mail
import dotenv
from django.utils.html import strip_tags
import re
import pandas as pd
import smtplib, ssl
import time
from .models import RoiData,UserInfo,TimeInterval
from django.http import JsonResponse
from django.views import View
from .apps import RoiCalculationConfig


from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

def start(): ### ITS A APSCHEDULAR FUNCTION :- WHICH IS ADD TIME INTERVAL FOR CALLING SCRIPT
    time = TimeInterval.objects.filter(id=1).first()
    if time:
        seted_time = time.time_interval
    else:
        seted_time = 90
    schedulers = BackgroundScheduler()
    schedulers.add_job(run_script,"interval",minutes=seted_time,id="interval_01",replace_existing=True)
    schedulers.start()

def setemail(request): #### SET SENDER EMAIL AND PASSWORD ### AND RECIEVER EMAIL ###
    if request.method == "POST":
        try:
            email = request.POST['Email']
            passwd = request.POST['Password']
            reciever = request.POST['reciever']
            user = UserInfo.objects.filter(id=1).first()
            if user:
                UserInfo.objects.filter(id=1).update(email=email, password=passwd)
            if reciever == "":
                UserInfo.objects.filter(id=1).update(rec_email=reciever)

            else:
                UserInfo.objects.create(email=email,password=passwd,rec_email=reciever)

            environment_variable = f"""EMAIL_HOST_USER={email.strip()}
EMAIL_HOST_PASSWORD={passwd.strip()}
EMAIL_RECIEVER_USER={reciever.strip()}""" ###### SET ENVIRONMENT VARIABLE FOR SETTINGS FILE
            with open('Vox_data_scraping/.env','w') as mail:
                mail.write(environment_variable)
        except:
            pass

    return redirect('/')



def run_script():   ### FINAL SCRIPT WHICH IS SCRAPPED DATA FROM RARITY TOOL SITE

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--start-maximized");
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    wait = WebDriverWait(browser, 20)

    with open('Vox_Scraped_data.csv','w') as fh:
        fh.write('')
    url_search = 'https://rarity.tools/collectvox?filters=%24buyNow%24On%3Atrue'
    browser.get(url_search)
    CSV_header = True
    time.sleep(10)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    page_container = soup.find('div',{'class':'flex flex-row justify-center lg:justify-end justify-end flex-initial flex-shrink-0'})
    page_box = page_container.find_all('div',{'class':'smallNoBtn'})[0]
    page_text = page_box.text
    intpage = str(page_text).strip().split(' ')[-1]
    final_page = int(intpage)


    VOX_RANK_GSP = []
    VOX_OPENSEA_RANK_GSP = []
    VOX_SCORE_GSP = []
    VOX_DAILY_INCOME_GSP = []
    VOX_DESCRIPTION_GSP = []
    VOX_BUY_NOW_USD_GSP =[]
    FINAL_ROI_GSP = []

    for i in range(1,2):

        PriceOfVox = []
        VoxRarityRank = []
        VoxRarityScoreList = []
        VoxAllLink = []
        VOX_LESS_LIST = []
        VOX_RANK_LESS = []
        VOX_ROI_LESS = []
        VOX_LINK = []
        Total_ROI = []

        time.sleep(10)
        browser.execute_script("window.scrollTo(0, 1000)")
        Main_Container = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[7]')
        page_input_tag = Main_Container.find_element_by_class_name('smallNoBtn')
        page_input = page_input_tag.find_element_by_tag_name('input')
        page_input.clear()
        page_input.send_keys(i)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        all_links = soup.find('div',{'class':'flex flex-row items-start justify-between'})

        ethrprice = ethereum_price.ethr() # Ethereum Price
        tawncoinprice =  tawncoin.tawn() #  Tawn Coin Price
        particular_vox = all_links.find_all('div',{'class':'overflow-hidden rounded-md m-0.5'})

        for img in particular_vox:
            vox_link = img.a['href']
            browser.get('https://rarity.tools'+vox_link)
            VoxAllLink.append(vox_link) # All Vox Links For
            time.sleep(5)

            soup = BeautifulSoup(browser.page_source, 'html.parser') ## NEW PARTICULAR VOX PAGE SOUP
            try:
                vox_rank_container = soup.find('span',{'class':'font-bold whitespace-nowrap'})
                vox_rank = vox_rank_container.text.split(' ')[-1]   ## FINAL VOX RANK
                VoxRarityRank.append(vox_rank)
                VOX_RANK_GSP.append(vox_rank)
                vox_price = soup.find('div',{'class':'h-full font-bold text-green-500'})
            except:
                continue

            try:
                vox_price_int = str(vox_price.text).replace('ETH','').strip() ### FINAL VOX PRICE
                PriceOfVox.append(vox_price_int)
            except:
                continue

            try:
                VoxRarityScore = soup.find('div',{'class':'px-2 mx-1 mb-0 text-lg font-extrabold text-green-500 bg-white rounded-md dark:bg-gray-800'})
                VRSP = str(VoxRarityScore.text).strip() #### VOX RARITY RANK SCORE
                VoxRarityScoreList.append(VRSP)
                VOX_SCORE_GSP.append(VRSP)
            except:
                continue

            try:
                VOX_OPENSEA = soup.find('div',{'class':'text-lg font-bold text-left text-pink-700 dark:text-gray-300'})
                VOX_OPENSEA_STR = VOX_OPENSEA.text
                FINAL_VOX_OPENSEA = VOX_OPENSEA_STR.strip().split(' ')[-1] ##### VOX OPENSEA RANK
                VOX_OPENSEA_RANK_GSP.append(FINAL_VOX_OPENSEA)
            except:
                continue

            try:
                hyper_link_opensea = soup.find('div',{'class':'mx-3 mt-1 mb-3'})
                HYPER_LINK_OPENSEA = hyper_link_opensea.a['href']       ### VOX OPENSEA RANK LINKS
            except:
                continue
            try:
                FINAL_VOX_NAME = VOX_OPENSEA_STR.strip().split('VOX')[0]  #### VOX NAME
                VOX_DESCRIPTION_GSP.append(FINAL_VOX_NAME)
            except:
                continue
            try:
                buy_now_usd = float(ethrprice) * float(vox_price_int)
                BUY_NOW_USD = format(buy_now_usd,'.2f')  ## BUY NOW USD = ETHEREUM_PRICE * VOX_PRICE
                VOX_BUY_NOW_USD_GSP.append(BUY_NOW_USD)
            except:
                continue

            try:
                vox_daily_income = float(tawncoinprice) * float(VRSP)
                VOX_DAILY_INCOME = format(vox_daily_income,'.2f') ## DAILY_INCOME = TAWNCOIN_PRICE * VOX_RANK_SCORE
                VOX_DAILY_INCOME_GSP.append(VOX_DAILY_INCOME)
            except:
                continue

            try:
                roi = buy_now_usd/vox_daily_income
                finlroi = format(roi,'.6f')
                Total_ROI.append(finlroi) ### FINAL ROI DATA
                FINAL_ROI_GSP.append(finlroi)

                if int(roi) <= int(200):
                    VOX_RANK_LESS.append(FINAL_VOX_OPENSEA)
                    VOX_LESS_LIST.append(vox_rank)
                    VOX_ROI_LESS.append(finlroi)
                    VOX_LINK.append('https://rarity.tools'+vox_link)


                data = RoiData.objects.filter(vox_rank=vox_rank)
                if data:
                    current_date = datetime.now()
                    data.update(vox_rarity_score=VRSP,buy_now_usd=BUY_NOW_USD,daily_income=VOX_DAILY_INCOME,total_roi=finlroi,date_time=current_date) ### UPDATE ALL DATA WHEN SCRIPT RUN SECOND TIME
                else:
                    current_date = datetime.now()
                    RoiData.objects.create(vox_rank=vox_rank,vox_id_opensea=FINAL_VOX_OPENSEA,vox_rarity_score=VRSP,daily_income=VOX_DAILY_INCOME,vox_description=FINAL_VOX_NAME,buy_now_usd=BUY_NOW_USD,total_roi=finlroi) ### IF DATA NOT EXIST IN DATA BASE THEN ITS CREATE NEW ENTRY FOR NEW VOX
                VoxDict = {"Rarity_Rank":'=HYPERLINK("https://rarity.tools'+vox_link+'","'+vox_rank+'")',"Vox_Id_opensea":'=HYPERLINK("'+HYPER_LINK_OPENSEA+'","'+FINAL_VOX_OPENSEA+'")',"Vox_Rarity_score":'=HYPERLINK("https://rarity.tools'+vox_link+'","'+vox_rank+'")',"Daily_Income":[VOX_DAILY_INCOME],"Descreption":'=HYPERLINK("https://rarity.tools'+vox_link+'","'+FINAL_VOX_NAME+'")',"Buy_Now_USD":[BUY_NOW_USD],"ROI":[finlroi]}
                df = pd.DataFrame(VoxDict)
                df.to_csv('Vox_Scraped_data.csv',mode='a',index=False,header=CSV_header)