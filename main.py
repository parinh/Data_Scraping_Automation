from bs4 import BeautifulSoup
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv



#set
chrome_options = Options()

# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = amazon-official-store]->>")
ss = 2
print ("Enter the url for the selected site.. ->>")
# base_url = input()
base_url = "https://www.amazon.com/s?k=garlic&ref=nb_sb_noss_2"

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
items_rating, img_src ,items_cost = [],[],[]
item_name, items_sold, discount_percent = [], [], []
items_review , item_id= [],[]

c=[]

#####################################################################################################################

#get all item in shopee na
def getDataFromPostForShopee(html):
    print("get data form shopee")
    soup = BeautifulSoup(html, "html.parser")
    for item_n in soup.find_all('div',  class_= "col-xs-2-4 shopee-search-item-result__item"):
        getItemDataForShopee(item_n)

#get all item in amazon search
def getDataFromPostForAmazonSearch(html):
    print ("get data..")
    soup = BeautifulSoup(html, "html.parser")
    for item_n in soup.find_all('div',  class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'):
        getItemDataForAmazonSearch(item_n)


    csv_count = 0
    with open('myfile.csv', 'w', newline='') as csvfile:
        head_csv = ["num","id","name","price","rating","review","img_src"]
        thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
        thewriter.writeheader()

        for i in range(len(item_name)):
            csv_count += 1
            thewriter.writerow({"num": csv_count,"id": item_id[i],"name": item_name[i],"price": items_cost[i],"rating": items_rating[i],"review":items_review[i],"img_src":img_src})

        
    #     mywriter = csv.writer(file)
    #     mywriter.writerow(head_csv)
    #     mywriter.writecolumn(head_csv)
    #     mywriter.writerow(item_id)
    #     mywriter.writerow(item_name)
    #     mywriter.writerow(items_cost)
    #     mywriter.writerow(items_rating)
    #     mywriter.writerow(items_review)
    #     mywriter.writerow(img_src)

        
        

#sort data form all item na
def getItemDataForShopee(soup):

    # Get Name
    for item_n in soup.find_all('div', class_='yQmmFK _1POlWt _36CEnF'):
        item_name.append(item_n.text)
        print(item_n.get_text())

    # Price
    for item_c in soup.find_all('div', class_='WTFwws _1lK1eK _5W0f35'):
        items_cost.append(item_c.text)
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
    name = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-base-plus.a-color-base.a-text-normal" )
    if (name):
        item_name.append(name.text)
        # print(name.get_text())
    else:
        item_name.append("no name")
        # print("no name")

    #item id
    item_code = soup['data-asin']
    if (item_code):
        item_id.append(item_code)
    else:
        item_id.append("no data")
    
    # Price
    price = soup.select_one("span.a-price > span.a-offscreen")
    if (price):
        items_cost.append(price.text)
        # print(price.get_text())
    else:
        items_cost.append("out of stock")
        # print("out of stock")

    # rating
    rating = soup.select_one("i > span.a-icon-alt")
    if (rating):
        items_rating.append(rating.text)
        # print(rating.get_text())
    else:
        items_rating.append("no rating found")
        # print("no rating found")

    #review
    review = soup.select_one("a.a-link-normal > span.a-size-base")
    if (review):
        items_review.append(review.text)
        # print(review.get_text())
    else:
        items_review.append("no review")
        # print("no review")
        
    imgs = soup.select_one("img.s-image")
    img_src.append(imgs['src'])
    # print(imgs['src'])

    # print ("###########################")

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




