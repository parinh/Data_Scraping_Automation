from os import name
import re
from bs4 import BeautifulSoup
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from tocsv import Tocsv



#set
chrome_options = Options()

# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = amazon-official-store]->>")
ss = int(input())

#page count
print ("enter number of pages")
page_count = int(input())

print ("Enter the url for the selected site.. ->>")
# page = 1
# base_url = input() + "&page=" +str(page)
base_url = input() 
# print (base_url)

count=0


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
delay = 5 
items_rating, img_src ,items_cost = [],[],[]
item_name, items_sold, discount_percent = [], [], []
items_review , item_id , items_form= [],[], []
item_url = []
products = []
csv = Tocsv("myfile.csv")

c=[]

#####################################################################################################################

#get all item in shopee na
def getDataFromPostForShopee(html):
    print("get data form shopee")
    soup = BeautifulSoup(html, "html.parser")
    #bigloop
    for item_n in soup.select('div[data-sqe=item]'):
        if item_n.select_one('div.shopee-image-placeholder'):
            continue
        else:
            data = getItemDataForShopee(item_n)
            products.append(data)

#get all item in amazon search
def getDataFromPostForAmazonSearch(html):
    print ("get data..")
    soup = BeautifulSoup(html, "html.parser")
    #big loop
    for item_n in soup.select('div[data-component-type=s-search-result]'):
        data = getItemDataForAmazonSearch(item_n)
        products.append(data)
        
        

#sort data form all item na
def getItemDataForShopee(soup):

    _name = 'no name'
    _price = 'no price'
    _sold = 'no sold'
    _from = 'no from'
    _image = 'no image'
    _url = 'no url'
    _type = 'general'

    # Get Name
    name = soup.select_one("div._1nHzH4 > div.PFM7lj > div.yQmmFK._1POlWt._36CEnF" )
    if (name):
        item_name.append(name.text)
        _name = name.text
        print(name.get_text())
    else:
        item_name.append("no name")
        print("no name")
    # for item_n in soup.find_all('div', class_='yQmmFK _1POlWt _36CEnF'):
    #     item_name.append(item_n.text)
    #     print(item_n.get_text())

    # Price
    price = soup.select_one("div.WTFwws._1lK1eK._5W0f35")
    if (price):
        items_cost.append(price.text)
        _price = price.text
        print(price.get_text())
    else:
        items_cost.append("no cost")
        print("no cost")
    # for item_c in soup.find_all('div', class_='WTFwws _1lK1eK _5W0f35'):
    #     items_cost.append(item_c.text)
    #     print(item_c.get_text())

    #type
    __type = soup.select_one("div.Oi0pcf.KRP-a_ > span._2_d9RP")
    if(__type):
        _type = __type.text
    else:
        print("general")

    __type = soup.select_one("div._1qt0vU > div.Oi0pcf._3Bekkv")
    print(__type)
    if(__type):
        _type = "shopee mall"
    else:
        print("general")

    # sold/month
    sold = soup.select_one("div.go5yPW")
    if (sold.text):
        items_sold.append(sold.text)
        _sold = int((sold.text).split(" ")[1])
        print(sold.get_text())
    else:
        _sold = "no sold"
        print("no item sold")

    #from
    __from = soup.select_one("div._2CWevj")
    if (__from):
        items_form.append(__from.text)
        _from = __from.text
        print(__from.get_text())
    else:
        items_form.append("no data")
        print("no data")    

    # find img path
    imgs = soup.select_one("div._25_r8I._2SHkSu > img")
   
    try:
        img_src.append(imgs['src'])
        _image = imgs['src']
        print (imgs['src'])
    except:
        print('no image source')

    #url
    url = soup.select_one("a")
    item_url.append("https://shopee.co.th/"+url['href'])
    _url = "https://shopee.co.th/"+url['href']
    print(url['href'])

    return {
        "name" : _name,
        "price" : _price,
        "sold": _sold,
        "from" :_from,
        "img_src":_image,
        "url" :_url,
        "type" : _type
    }
    
    # for imgs in soup.find_all('div', class_ = '_25_r8I _2SHkSu'):
    #     print(imgs.select("img")[0]['src'])

# #################################################################################################

#sort data form all item na
def getItemDataForAmazonSearch(soup):

    _name = 'no name'
    _id = 'no id'
    _price = 'out of stock'
    _rating = 'no rating'
    _review = 'no review'
    _image = 'no image'
    _url = 'no url'
    _bestseller = 'not be a best'

    # Get Name
    name = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-base-plus.a-color-base.a-text-normal" )
    if (name):
        item_name.append(name.text)
        _name = name.text
        # print(name.get_text())
    else:
        item_name.append("no name")
        # print("no name")

    #item id
    item_code = soup['data-asin']
    if (item_code):
        item_id.append(item_code)
        _id = item_code
    else:
        item_id.append("no data")
    
    # Price
    price = soup.select_one("span.a-price > span.a-offscreen")
    if (price):
        items_cost.append(price.text)
        _price = price.text
        # print(price.get_text())
    else:
        items_cost.append("out of stock")
        # print("out of stock")

    # rating
    rating = soup.select_one("i > span.a-icon-alt")
    if (rating):
        items_rating.append(rating.text)
        _rating = float((rating.text).split(" ")[0])
        # print(rating.get_text())
    else:
        items_rating.append("no rating found")
        # print("no rating found")

    #review
    review = soup.select_one("a.a-link-normal > span.a-size-base")
    if (review):
        items_review.append(review.text)
        _review = review.text
        # print(review.get_text())
    else:
        items_review.append("no review")
        # print("no review")
        
    imgs = soup.select_one("img.s-image")
    if (imgs):
        img_src.append(imgs['src'])
        _image = imgs['src']
    # print(imgs['src'])

    #best?
    bestseller = soup.select_one("div.a-row.a-badge-region > span.a-badge > span.a-badge-label > span.a-badge-label-inner.a-text-ellipsis > span.a-badge-text ")
    print(bestseller)
    if(bestseller):
        _bestseller = bestseller.text
    else:
        print("no bestseller")

    #post url
    post_url = soup.select_one("span.rush-component > a.a-link-normal.s-no-outline")

    if(post_url):
        item_url.append("https://www.amazon.com/"+post_url['href'])
        _url = "https://www.amazon.com/"+post_url['href']

    return {
         "name": _name,
        "id": _id,
        "price": _price, 
        "rating": _rating, 
        "review": _review,
        "img_src": _image,
        "url": _url,
        "bestseller" : _bestseller
    }
    

    # print ("###########################")

# #################################################################################################

# shopee set
if(ss == 1):
    header_field = ["num","name","price","type","sold","from","img_src","url"]
    page=0
    csv.setHeader(header_field)

    while page<page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            print ("Page is ready")
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

            getDataFromPostForShopee(html)
            page+=1
                        
             # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")

    csv.addDataForShopee(products)



# amazon search set
elif (ss == 2):
    header_field = ["num","id","name","price","rating","review","img_src","url","rank"]
    page=1
    csv.setHeader(header_field)

    while page<=page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            print ("Page is ready")
            
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

            getDataFromPostForAmazonSearch(html)
            page+=1
                # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")
    csv.addDataForAmazon(products)

browser.close()




