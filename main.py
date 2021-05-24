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

#set
chrome_options = Options()
shopee = Shopee() 
amazon = Amazon()
pantip = Pantip()


# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = pantip]->>")
ss = int(input())

print ("enter number of pages")
page_count = int(input())

print ("Enter the url for the selected site.. ->>")
# page = 1
# base_url = input() + "&page=" +str(page)
base_url = input() 
# base_url = "https://www.amazon.com/s?k=chicken&ref=nb_sb_noss_2"

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
browser.get(base_url)
delay = 5 

# for shopee
if(ss == 1):
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
    page=0
    while page<=page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # browser.execute_script("window.scrollTo(0,  window.scrollY + 200);")
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
# elif (ss == 3):
#     browser.get(base_url)
#     WebDriverWait(browser, delay)
#     print ("Page is ready")
#     sleep(5)

#     browser.execute_script("window.scrollTo(0, 0);")
#     html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    
#     pantip.getPosts(html)
    
    

# test pantip
elif(ss == 3):
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
        ch += sh/3
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, "html.parser")

    pantip.getPosts(soup)
    
    print(len(pantip.posts))
browser.close()




