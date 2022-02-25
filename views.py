from datetime import datetime
from django.shortcuts import render,redirect
from roi_calculation import ethereum_price
from roi_calculation import tawncoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
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

def start():
    time = TimeInterval.objects.filter(id=1).first()
    if time:
        seted_time = time.time_interval
    else:
        seted_time = 90
    print(seted_time,">>>>>>>>>>>>>>>>>>>Time Interval")
    schedulers = BackgroundScheduler()
    schedulers.add_job(run_script,"interval",minutes=seted_time,id="interval_01",replace_existing=True)
    schedulers.start()

def setemail(request):
    if request.method == "POST":
        try:
            email = request.POST['Email']
            passwd = request.POST['Password']
            reciever = request.POST['reciever']
            user = UserInfo.objects.filter(id=1).first()
            if user:
                UserInfo.objects.filter(id=1).update(email=email, password=passwd)
            if reciever != "":
                UserInfo.objects.filter(id=1).update(rec_email=reciever)

            else:
                UserInfo.objects.create(email=email,password=passwd,rec_email=reciever)

            environment_variable = f"""EMAIL_HOST_USER={email.strip()}
EMAIL_HOST_PASSWORD={passwd.strip()}
EMAIL_RECIEVER_USER={reciever.strip()}"""
            with open('Vox_data_scraping/.env','w') as mail:
                mail.write(environment_variable)
        except:
            pass
        
    return redirect('/')



def run_script():
    print('Called First')
    with open('roi_calculation/Vox_Scraped_data.csv','w') as fh:
           fh.write('')
            
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--start-maximized");
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    wait = WebDriverWait(browser, 20)

    with open('roi_calculation/Vox_Scraped_data.csv','w') as fh:
        reader = fh.write('')
    # print(file_data)
    # rng = file_data/48
    # print(rng,'range')
    url_search = 'https://rarity.tools/collectvox?filters=%24buyNow%24On%3Atrue'
    browser.get(url_search)
    CSV_header = True
    for i in range(1,19):
        print(i)
        # print(i)
        # with open('roi_calculation/Vox_Scraped_data.csv','r') as fh:
        #     reader = fh.readlines()
        #     file_data = len(reader)

        # if file_data == 0:
        #     CSV_header = True
        # else:
        #     CSV_header = False

        PriceOfVox = []
        VoxRarityRank = []
        VoxRarityScoreList = []
        VoxAllLink = []
        VOX_LESS_LIST = []
        VOX_RANK_LESS = []
        VOX_ROI_LESS = []
        VOX_LINK = []
        Total_ROI = []
        # print('wait')
        time.sleep(10)
        # print('start')
        browser.execute_script("window.scrollTo(0, 1000)")
        Main_Container = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div[2]/div[7]')
        page_input_tag = Main_Container.find_element_by_class_name('smallNoBtn')
        page_input = page_input_tag.find_element_by_tag_name('input')
        page_input.clear()
        page_input.send_keys(i)
        # print(page_input)
        # time.sleep(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        all_links = soup.find('div',{'class':'flex flex-row items-start justify-between'})
        # print(all_links,"<<<<<<<<<<all_links")
        # print(len(all_links),'Number Of Vox')
        try:
            ethrprice = ethereum_price.ethr() # Ethereum Price
            tawncoinprice =  tawncoin.tawn() #  Tawn Coin Price
            particular_vox = all_links.find_all('div',{'class':'overflow-hidden rounded-md m-0.5'})
            # print(particular_vox.a['href'],"<<<<<<<<<<<<<particular_vox")
            # print(len(vox_rank),'Vox Rank')
            # print(len(lnk))
            for img in particular_vox:
                vox_link = img.a['href']
                browser.get('https://rarity.tools'+vox_link)
                VoxAllLink.append(vox_link) # All Vox Links For 
                time.sleep(5)

                soup = BeautifulSoup(browser.page_source, 'html.parser')
                
                vox_price = soup.find('div',{'class':'h-full font-bold text-green-500'})
                vox_price_int = str(vox_price.text).replace('ETH','').strip()
                print(vox_price_int,'<<<<<<<< VOX PRICE')
                PriceOfVox.append(vox_price_int)
                
                vox_rank_container = soup.find('span',{'class':'font-bold whitespace-nowrap'})
                vox_rank = vox_rank_container.text.split(' ')[-1]
                print(vox_rank,'<<<<<<>>>>>>')
                VoxRarityRank.append(vox_rank)

                VoxRarityScore = soup.find('div',{'class':'px-2 mx-1 mb-0 text-lg font-extrabold text-green-500 bg-white rounded-md dark:bg-gray-800'})
                VRSP = str(VoxRarityScore.text).strip()
                # print(VRSP)
                VoxRarityScoreList.append(VRSP)

                VOX_OPENSEA = soup.find('div',{'class':'text-lg font-bold text-left text-pink-700 dark:text-gray-300'})
                VOX_OPENSEA_STR = VOX_OPENSEA.text
                FINAL_VOX_OPENSEA = VOX_OPENSEA_STR.strip().split(' ')[-1]
                # print(FINAL_VOX_OPENSEA,'<<<<<<<<<<<<<')

                hyper_link_opensea = soup.find('div',{'class':'mx-3 mt-1 mb-3'})
                HYPER_LINK_OPENSEA = hyper_link_opensea.a['href']
                print(HYPER_LINK_OPENSEA,'<<<<<<<<>>>>>>>>')

                FINAL_VOX_NAME = VOX_OPENSEA_STR.strip().split('VOX')[0]
                print(FINAL_VOX_NAME,'<<<<<<<<<<<<<<<')

                buy_now_usd = float(ethrprice) * float(vox_price_int)
                BUY_NOW_USD = format(buy_now_usd,'.2f')

                vox_daily_income = float(tawncoinprice) * float(VRSP)
                VOX_DAILY_INCOME = format(vox_daily_income,'.2f')


                roi = buy_now_usd/vox_daily_income
                finlroi = format(roi,'.6f')
                Total_ROI.append(finlroi)

                if int(roi) <= int(200):
                    VOX_RANK_LESS.append(FINAL_VOX_OPENSEA)
                    VOX_LESS_LIST.append(vox_rank)
                    VOX_ROI_LESS.append(finlroi)
                    VOX_LINK.append('https://rarity.tools'+vox_link)  
                    
                data = RoiData.objects.filter(vox_rank=vox_rank)
                if data:
                    current_date = datetime.now()
                    # print(data,"<<<<<<<<<<")
                    top_roi = data.first().top_roi_rank
                    if float(top_roi) < float(roi):
                        data.update(top_roi_rank=finlroi)
                    data.update(vox_price=vox_price_int,vox_rarity_score=VRSP,eth_price=ethrprice,tawncoin_price=tawncoinprice,buy_now_usd=BUY_NOW_USD,daily_income=VOX_DAILY_INCOME,total_roi=finlroi,date_time=current_date)
                else:
                    current_date = datetime.now()
                    RoiData.objects.create(top_roi_rank=finlroi,vox_rank=vox_rank,vox_id_opensea=FINAL_VOX_OPENSEA,vox_rarity_score=VRSP,vox_description=FINAL_VOX_NAME,buy_now_usd=BUY_NOW_USD,vox_price=vox_price_int,make_offer=0,eth_price=ethrprice,tawncoin_price=tawncoinprice,daily_income=VOX_DAILY_INCOME,total_roi=finlroi)
                VoxDict = {"Top_Roi_Rank":[finlroi],"Rarity_Rank":'=HYPERLINK("https://rarity.tools'+vox_link+'","'+vox_rank+'")',"Vox_Id_opensea":'=HYPERLINK("'+HYPER_LINK_OPENSEA+'","'+FINAL_VOX_OPENSEA+'")',"Vox_Rarity_score":'=HYPERLINK("https://rarity.tools'+vox_link+'","'+vox_rank+'")',"Descreption":'=HYPERLINK("https://rarity.tools'+vox_link+'","'+vox_rank+'")',"Buy_Now_USD":[BUY_NOW_USD],"Buy_Now_ETH":[vox_price_int],"Make_Offer":[0],"ETH_Price":[ethrprice],"Town_Coine_Price":[tawncoinprice],"Daily_Income":[VOX_DAILY_INCOME],"ROI":[finlroi]}
                df = pd.DataFrame(VoxDict)
                df.to_csv('roi_calculation/Vox_Scraped_data.csv',mode='a',index=False,header=CSV_header)
                CSV_header = False
        except:
            pass

    ################## EMail Send Started

    




   
    Data_List =[]
    for (i,j,k,l) in zip(VOX_RANK_LESS,VOX_LESS_LIST,VOX_ROI_LESS,VOX_LINK):
        data_dict = {"opensea":i,"rank":j,"roi":k,"link":l}
        Data_List.append(data_dict)




    if len(VOX_LESS_LIST) != 0:
        EMAIL_HOST = settings.EMAIL_HOST_USER
        EMAIL_PASSWORD = settings.EMAIL_HOST_PASSWORD
        sub = 'Alert ROI is LessThan 200!!'
        # msg = inner_row
        msg_html = render_to_string('mail_format.html', {'email':EMAIL_HOST,'subject':sub,'data':Data_List})
        palnning = strip_tags(msg_html)
        print(palnning)

        send_mail(sub,palnning,
        'VOX ROI' +'<'+settings.EMAIL_HOST_USER+'>',
        [settings.EMAIL_RECIEVER_USER],
        html_message=msg_html,
        )
        browser.close()
    else:
        pass
        # for vox in VoxAllLink:
        #     print(vox)
        #     browser.get('https://rarity.tools'+vox)
        #     time.sleep(3)
        #     soup = BeautifulSoup(browser.page_source, 'html.parser')
        #     VoxRarityScore = soup.find('div',{'class':'px-2 mx-1 mb-0 text-lg font-extrabold text-green-500 bg-white rounded-md dark:bg-gray-800'})
        #     VRSP = str(VoxRarityScore.text).strip()
        #     VoxRarityScoreList.append(VRSP)
        #     print(VRSP)

        # for (vxprice,vxscore) in zip(PriceOfVox,VoxRarityScoreList):
        #     BUY_NOW_USD = float(ethrprice) * float(vxprice)
        #     VOX_DAILY_INCOME = float(tawncoinprice) * float(vxscore)
        #     roi = BUY_NOW_USD/VOX_DAILY_INCOME
        #     finlroi = format(roi,'.6f')
        #     Total_ROI.append(finlroi)
        #     print(finlroi)
        # print(len(VoxAllLink))
        # print(len(VoxRarityRank))
        # print(len(PriceOfVox))
        # print(len(VoxRarityScoreList))


        # for (rank,vprc,vscore,roi) in zip(VoxRarityRank,PriceOfVox,VoxRarityScoreList,Total_ROI):


class setup(View):

    @classmethod
    def settime(self,request):
        try:
            time_int = request.POST['intervaltime']
            time = TimeInterval.objects.filter(id=1).first()
            if time:
                TimeInterval.objects.filter(id=1).update(time_interval=time_int)
            else:
                TimeInterval.objects.create(time_interval=time_int)
        except:
            pass
        
        RoiCalculationConfig.ready(self)
        
        return redirect('/')

def homepage(request):
    # start()
    # print(settings.EMAIL_HOST_USER,'<<<<<<<<<<<<<')
    # print(settings.EMAIL_HOST_PASSWORD)
    # VOX_LESS_LIST = ['#7','#9','#13','#18','#29']
    # VOX_OPENSEA_RANK_LESS = [166.497,222.723,193.078,777.845,960.531]
    # VOX_ROI_LESS = [166.497486,222.723909,193.078099,777.845923,960.531403]



    # inner_row = ''
    # Data_List = []
    # for (i,j,k) in zip(VOX_OPENSEA_RANK_LESS,VOX_LESS_LIST,VOX_ROI_LESS):
    #     data_dict = {"opensea":i,"rank":j,"roi":k}
    #     Data_List.append(data_dict)
    #     # TABLE_FORM = '<td>{0}</td><td>{1}</td><td>{2}</td>'.format(i,j,k)
    #     # Data_List.append(TABLE_FORM)
    #     # Data_List.append(TABLE_FORM)

    # # FINAL_MSG = inner_row

    # EMAIL_HOST = settings.EMAIL_HOST_USER
    # EMAIL_PASSWORD = settings.EMAIL_HOST_PASSWORD
    # sub = 'Alert ROI is LessThan 200!!'
    # # msg = inner_row
    # msg_html = render_to_string('mail_format.html', {'email':EMAIL_HOST,'subject':sub,'data':Data_List})
    # palnning = strip_tags(msg_html)
    # print(palnning)

    # send_mail(sub,palnning,
    # 'VOX ROI' +'<'+settings.EMAIL_HOST_USER+'>',
    # [settings.EMAIL_HOST_USER],
    # html_message=msg_html,
    # )
    # print('Sended')
    user = UserInfo.objects.filter(id=1).first()
    return render(request,'index.html',{"user":user})

def error_400(request,exception):
    data ={}
    return render(request,'400_error.html',data)

def error_403(request,exception):
    data ={}
    return render(request,'403_error.html',data)

def error_404(request,exception):
    data ={}
    return render(request,'404_error.html',data)

def error_500(request):
    data ={}
    return render(request,'500_error.html',data)
