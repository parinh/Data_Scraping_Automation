from bs4 import BeautifulSoup
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from shopee import *


#get all item in shopee na
def getDataFromPostForShopee(html):
    soup = BeautifulSoup(html, "html.parser")
    for item_n in soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'):
        getItemDataForShopee(item_n)

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

#set
chrome_options = Options()

# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = amazon-official-store]->>")
ss = int(input())
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
browser = webdriver.Chrome(executable_path = r"C:/Users/Bell/Downloads/chromedriver_win32/chromedriver.exe",
                          options = chrome_options)
browser.get(base_url)
delay = 5 

item_all = []

item_cost, item_rt, img_src = [],[],[]
item_name, items_sold, discount_percent = [], [], []

c=[]

# for shopee
if(ss == 1):
    while True:
        try:
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

            getDataFromPostForShopee(html)

            # c = getDataFromPostForShopee(html)

            # for i in c:
            #     for j in i:
            #         print(j)
            #     print ("\n")
            



            #print(html)11
            # soup = BeautifulSoup(html, "html.parser")

            # # # find_all() returns an array of elements. 
            #  # We have to go through all of them and select that one you are need. And than call get_text()
            # for item_n in soup.find_all('div', class_='yQmmFK _1POlWt _36CEnF'):
            #      item_name.append(item_n.text)
            #      print(item_n.get_text())

            #  # find the price of items
            # for item_c in soup.find_all('div', class_='WTFwws _1lK1eK _5W0f35'):
            #      item_cost.append(item_c.text)
            #      print(item_c.get_text())

            #  # find total number of items sold/month *********
            # for items_s in soup.find_all('div',class_ = 'go5yPW'):
            #      items_sold.append(items_s.text)
            #      print(items_s.get_text())
                 

            # # find img path
            # for imgs in soup.find_all('div', class_ = 'customized-overlay-image'):
            #     # soupInner = bs4.BeautifulSoup(imgs.get_text(), "html.parser")
            #     print(imgs.select("img")[0]['src'])
            #     # for imageSrc in soupInner.find_all('img'):
                #      print(imageSrc['src'])

                #  print(img.get_text())

                        
            break # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")




# for amazon search
elif (ss == 2):
    while True:
        try:
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            #print(html)
            soup = BeautifulSoup(html, "html.parser")

            # find_all() returns an array of elements. 
            # We have to go through all of them and select that one you are need. And than call get_text()
            for item_n in soup.find_all('span', class_='a-size-base-plus'):
                item_name.append(item_n.text)
                print(item_n.get_text())

            # find the price of items

            for item_c in soup.find_all('span',class_ = 'a-price'):
                item_cost.append(item_c.text)
                print(item_c.get_text())

            # rating
            for items_rt in soup.find_all('span',class_ = 'a-icon-alt'):
                items_rt.append(items_rt.text)
                print(items_rt.get_text())

            # # find total number of items sold/month != amazon
            # for items_s in soup.find_all('div',class_ = 'go5yPW"'):
            #     items_sold.append(items_s.text)
            #     print(items_s.get_text())

            # find item discount percent
            for dp in soup.find_all('span', class_ = 'a-price a-text-price'):
                discount_percent.append(dp.text)
                print("form -->"+(dp.get_text()))


                
            break # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")



# for amazon officail store
elif (ss == 3):
    while True:
        try:
            WebDriverWait(browser, delay)
            print ("Page is ready")
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            
            
            #print(html)
            soup = BeautifulSoup(html, "html.parser")

            # find_all() returns an array of elements. 
            # We have to go through all of them and select that one you are need. And than call get_text()
            for item_n in soup.find_all('a', class_='ProductGridItem__title__2C1kS'):
                item_name.append(item_n.text)
                print(item_n.get_text())

            # find the price of items
            for item_c in soup.find_all('span', class_='price style__xlarge__1mW1P ProductGridItem__buyPrice__6DIeT style__fixedSize__2cXU-'):
                item_cost.append(item_c.text)
                print(item_c.get_text())

            # rating
            for items_rt in soup.find_all('span',class_ = 'a-icon-alt'):
                items_rt.append(items_rt.text)
                print(items_rt.get_text())

            # # find total number of items sold/month != amazon
            # for items_s in soup.find_all('div',class_ = 'go5yPW"'):
            #     items_sold.append(items_s.text)
            #     print(items_s.get_text())

            # find item discount percent
            for dp in soup.find_all('span', class_ = 'price style__small__35Bk_ ProductGridItem__strikePrice__1TwIT style__strikethrough__1tKkI style__fixedSize__2cXU-'):
                discount_percent.append(dp.text)
                print("form -->"+(dp.get_text()))


                
            break # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")


browser.close()




