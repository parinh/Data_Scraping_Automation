from bs4 import BeautifulSoup
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep


#get all item in shopee na
def getDataFromPostForShopee(html):
    soup = BeautifulSoup(html, "html.parser")
    b=[]
    for item_n in soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'):
        # getItemDataForShopee(item_n)
        b.append(getItemDataForShopee(item_n))

    return b


#sort data form all item na
def getItemDataForShopee(soup):
    a=[]
    # Get Name
    for item_n in soup.find_all('div', class_='yQmmFK _1POlWt _36CEnF'):
        a.append(item_n.text)
        print(item_n.get_text())

    # Price
    for item_c in soup.find_all('div', class_='WTFwws _1lK1eK _5W0f35'):
        a.append(item_c.text)
        print(item_c.get_text())

    # find total number of items sold/month *********
    for items_s in soup.find_all('div',class_ = 'go5yPW'):
        a.append(items_s.text)
        print(items_s.get_text())

    #from
    for items_f in soup.find_all('div',class_ = '_2CWevj'):
        a.append(items_f.text)
        print(items_f.get_text())        

    # find img path
    for imgs in soup.find_all('div', class_ = '_25_r8I _2SHkSu'):
        a.append(imgs.select("img")[0]['src'])
        print(imgs.select("img")[0]['src'])

    return a

#################################################################################################