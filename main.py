from jd import JD
from lazada import Lazada
from selenium.webdriver.chrome.webdriver import WebDriver
from pantip import Pantip
from bs4 import BeautifulSoup
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from shopee import *
from amazon import *
from pantip import *
from tocsv import Tocsv
from jd import *
from facebook_scraper import *
from facebook import *

#set
chrome_options = Options()
shopee = Shopee() 
amazon = Amazon()
pantip = Pantip()
lazada = Lazada()
jd = JD()
facebook = Facebook()


# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = pantip][4= jd][5 = facebook]->>")
ss = int(input())

#close all popup
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument("disable-infobars")

# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
    })

#chrome driv ja
browser = webdriver.Chrome(executable_path = r"C:/Users/Bell/Downloads/chromedriver_win32/chromedriver.exe",
                          options = chrome_options)
# browser.get(base_url)
delay = 5 

# for shopee
if(ss == 1):
    print ("enter number of pages")
    page_count = int(input())

    print ("Enter the url for the selected site.. ->>")
    base_url = input() 

    page = 0
    while page<=page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 1);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 2);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 3);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 4);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 5);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 6);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 7);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 8);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 9);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 10);")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            shopee.getData(html)

            # for product in products:
            #     for data in product:
            #         print(data)
            #     print("##########")
            
            page+=1
        
         
        except TimeoutException:
            print ("Loading took too much time!-Try again")
    
    shopee.toCsv(shopee.products)



# for amazon search
elif (ss == 2):
    print ("enter number of pages")
    page_count = int(input())
    print ("Enter the url for the selected site.. ->>")
    base_url = input() 

    page=0
    while page<=page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 1);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 2);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 3);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 4);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 5);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 6);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 7);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 8);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 9);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 10);")
            sleep(5)
            print ("Page is ready")
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            amazon.getData(html)    

            # for product in products:
            #     for data in product:
            #         print(data)
            #     print("##########")
                
            page+=1
        except TimeoutException:
            print ("Loading took too much time!-Try again")
    
    amazon.toCsv(amazon.products)
    

#pantip
elif(ss == 3):
    print ("enter number of pages")
    page_count = int(input())
    print ("Enter the url for the selected site.. ->>")
    base_url = input() 
    browser.get(base_url)
    ch = 0 
    WebDriverWait(browser, delay)
    print ("Page is ready")
    sleep(5)
    browser.execute_script("window.scrollTo(0, 0);")
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")   
    soup = BeautifulSoup(html, "html.parser")
    while (page_count > len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')) ): 
        sh = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script("window.scrollTo(0, %d);"% ch)
        ch += sh/33

        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, "html.parser")

    pantip.getPosts(soup)
    
    pantip.toCsv(pantip.posts)


#JD
elif(ss == 4):
    print ("enter number of pages")
    page_count = int(input())
    print ("Enter the keyword for the selected site.. ->>")
    keyword = input()
    page = 0
    base_url = ("https://api.jd.co.th/client.action?body={'pagesize':'60','page':'" + str(page) +"','keyword':'" + keyword + "'}&functionId=search&client=pc&clientVersion=2.0.0&lang=th_TH&area=184549376-185008128-185008132-0")
    browser.get(base_url)
    
    while page<=page_count:
        try:
            # browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 1);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 2);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 3);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 4);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 5);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 6);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 7);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 8);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 9);")
            browser.execute_script("window.scrollTo(0, (document.body.scrollHeight /10) * 10);")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            jd.getProducts(html)

            
            page+=1
        
         
        except TimeoutException:
            print ("Loading took too much time!-Try again")

    jd.toCsv(jd.products)

#facebook
elif(ss == 5):
    print ("Enter page ->>")
    page_id = input()
    print("Enter number of pages")
    page_count = int(input())

    facebook.getPosts(page_id,page_count)
    print(len(facebook.posts))
    # for post in facebook.posts:
    #     print(post['text'])

    facebook.toCsv(facebook.posts)

   
     


browser.close()




