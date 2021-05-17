from bs4 import BeautifulSoup
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
# from shopee import *


#set
chrome_options = Options()

# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = amazon-official-store]->>")
ss = 2
print ("Enter the url for the selected site.. ->>")
# base_url = input()
base_url = "https://www.amazon.com/s?k=garlic&ref=nb_sb_noss"

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
browser = webdriver.Chrome(executable_path = r"/Users/mcmxcix/chromedriver",
                          options = chrome_options)
browser.get(base_url)
delay = 5 


item_cost, items_rating, img_src = [],[],[]
item_name, items_sold, discount_percent = [], [], []
items_review = []

c=[]

#####################################################################################################################

#get all item in shopee na
def getDataFromPostForShopee(html):
    print("get data form shopee")
    soup = BeautifulSoup(html, "html.parser")
    for item_n in soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'):
        getItemDataForShopee(item_n)

#get all item in amazon search
def getDataFromPostForAmazonSearch(html):
    print ("get data..")
    soup = BeautifulSoup(html, "html.parser")
    for item_n in soup.find_all('div',  class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'):
        getItemDataForAmazonSearch(item_n)

#sort data form all item na
def getItemDataForShopee(soup):

    # Get Name
    for item_n in soup.find_all('div', class_='yQmmFK _1POlWt _36CEnF'):
        item_name.append(item_n.text)
        print(item_n.get_text())

    # Price
    for item_c in soup.find_all('div', class_='WTFwws _1lK1eK _5W0f35'):
        item_cost.append(item_c.text)
        print(item_c.get_text())

    # find total number of items sold/month *********
    for items_s in soup.find_all('div',class_ = 'go5yPW'):
        items_sold.append(items_s.text)
        print(items_s.get_text())

    #from
    for items_f in soup.find_all('div',class_ = '_2CWevj'):
        items_f.append(items_f.text)
        print(items_f.get_text())        

    # find img path
    for imgs in soup.find_all('div', class_ = '_25_r8I _2SHkSu'):
        print(imgs.select("img")[0]['src'])

# #################################################################################################

#sort data form all item na
def getItemDataForAmazonSearch(soup):

    # Get Name
    item_n = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-base-plus.a-color-base.a-text-normal" )
    if (item_n):
        print(item_n.get_text())
    else:
        print("no name")

    # Price
    price = soup.select_one("span.a-price > span.a-offscreen")
    if (price):
        print(price.get_text())
    else:
        print("no price found")

    # rating
    rating = soup.select_one("i > span.a-icon-alt")
    if (rating):
        print(rating.get_text())
    else:
        print("no rating found")

    #review
    review = soup.select_one("a.a-link-normal > span.a-size-base")
    if (review):
        print(review.get_text())
    else:
        print("no review")
        
    imgs = soup.select_one("img.s-image")
    print(imgs['src'])

    print ("###########################")

# #################################################################################################

# shopee set
if(ss == 1):
    while True:
        try:
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

            getDataFromPostForShopee(html)
                        
            break # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")



# amazon search set
elif (ss == 2):
    while True:
        try:
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            #print(html)
            soup = BeautifulSoup(html, "html.parser")

            getDataFromPostForAmazonSearch(html)
                
            break # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")

browser.close()




