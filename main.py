#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from logging import exception
from os import name
import re
from bs4 import BeautifulSoup
# import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep, time
from tocsv import Tocsv
from lxml import html as htmllxml
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from os import path
from pythainlp import sent_tokenize, word_tokenize,Tokenizer
from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words
from facebook_scraper import *
import sys

#add new word to custom
newWords = ["ไม่ดี","ไม่พอใจ","ชั่วคราว","ต่อต้าน","เล่นวีดีโอ","บาดเจ็บ"]
custom_words_list = set(thai_words())
custom_words_list.update(newWords)
trie = dict_trie(dict_source=custom_words_list)
custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm',keep_whitespace=False)


#locate words file and append to array
positive_vocab = []
negative_vocab = []
swear_words = []

with open("/Users/mcmxcix/nodeJSDB/pythongetpostshopee1/words/negative-sentiment-words.txt", 'r',encoding='utf8') as f:
    for line in f:
        negative_vocab.append(line.rstrip())

with open("/Users/mcmxcix/nodeJSDB/pythongetpostshopee1/words/positive-sentiment-words.txt", 'r',encoding='utf8') as f:
    for line in f:
        positive_vocab.append(line.rstrip())
        
with open("/Users/mcmxcix/nodeJSDB/pythongetpostshopee1/words/swear-words.txt", 'r',encoding='utf8') as f:
    for line in f:
        swear_words.append(line.rstrip())

#set
chrome_options = Options()

# input url site
print ("select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = pantip][4 = JD][5 = FaceBook]->>")
ss = int(input())

#page count
print ("enter number of pages//posts")
page_count = int(input())

print ("Enter the keyword for the selected site.. ->>")
keyword = input()


count=0
post =0


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
item_url = []
products = []
csv = Tocsv("myfile.csv")

c=[]


def getDataFromPostForBedo(html):
    print("get data form shopee")
    soup = BeautifulSoup(html, "html.parser")
    data = {
        "group" : "",
        "thai_name" : ""
    }
    #bigloop
    for item in soup.select('ol[id=general_information] > li.metaContent-item'):
        if ("กลุ่มทรัพยากรชีวภาพ" in item.select_one("div.title").text):
            _group = item.select_one("div.value").text
            data["group"] = _group

        if ("ชื่อพันธุ์ไทย" in item.select_one("div.title").text):
            _thai_name = item.select_one("div.value").text
            data["thai_name"] = _thai_name
        
        else:  
            print("else")

    # data = getItemDataForBedo(item)
    print(data)
    products.append(data)

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
    print ("get data Amazon")
    soup = BeautifulSoup(html, "html.parser")
    #big loop
    for item_n in soup.select('div[data-component-type=s-search-result]'):
        data = getItemDataForAmazonSearch(item_n)
        products.append(data)

        
def getDataFormPostForPantip(html):
    print ("get data Pantip")
    soup = BeautifulSoup(html, "html.parser") 
    ch = 0 
    current_len = 0
    count = 0

    while (page_count > len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'))): 
        
        current_len = len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'))
        
        sh = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script("window.scrollTo(0, %d);"% ch)
        ch += sh/3
        # print(len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')))
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, "html.parser")
        print(len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')))
        if (current_len == len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'))):
            count += 1
            if (count == 100):
                break
        else :
            count = 0

 

    

    for item_n in soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'): 
        # print(sh)
        link = item_n['href']
        data = getItemDataForPantip(link)
        products.append(data)
        # print(type(ch))
        
#get all item in JD
def getDataFromPostForJD(html):
    print ("get data JD")
    soup = BeautifulSoup(html, "html.parser")
    #big loop
    item_n = soup.select_one('pre')
    info = json.loads(item_n.text)
    # print(len(info['wareInfo']))
    for item in info['wareInfo'] :
        # print (item['wname'])
        data = getItemDataForJD(item)
        products.append(data)

def getDataFromPostForFacebook(keyword,page_count):
    print ("get data from facebook")

    
    try:
        if ( page_count <= 100):
            for post in get_posts(keyword,pages = page_count, page_limit = 100,timeout = 10,options = {"posts_per_page": 10}):
                print("processing..")
                data = getItemDataForFacebook(post)
                products.append(data)
            print("get post succ")

        else:
            print("cant get posts // pages limit was set on 100 ")
    except:
        print("get post error")
        # print("Unexpected error:", sys.exc_info()[0])

#sort data form all item na
def getItemDataForShopee(soup):

    _name = 'no name'
    _price = 0
    _sold = 'no sold'
    _from = 'no from'
    _image = 'no image'
    _url = 'no url'
    _type = 'general'
    _star = 0
    _id = "no id"

    # Get Name
    name = soup.select_one("div._1nHzH4 > div.PFM7lj > div.yQmmFK._1POlWt._36CEnF" )
    if (name):
        _name = name.text
        # print(name.get_text())

    # Price
    price = soup.select_one("div.WTFwws._1lK1eK._5W0f35")
    if (price):
        _price = float("".join((price.text).split(" ")[0].split("฿")[1].split(",")))

        print(_price)
        
    #type
    __type = soup.select_one("div.Oi0pcf.KRP-a_ > span._2_d9RP")
    if(__type):
        _type = __type.text

    __type = soup.select_one("div._1qt0vU > div.Oi0pcf._3Bekkv")
    # print(__type)
    if(__type):
        _type = "shopee mall"

    # sold/month
    sold = soup.select_one("div.go5yPW")
    if (sold.text):
        
        if "พัน" not in sold.text:
            _sold = float((sold.text).split(" ")[1])
            # print(_sold)
        
        else:
            _sold = float((sold.text).split(" ")[1].split("พัน")[0]) * 1000
            # print(_sold)
    else:
        _sold = "no sold"

    #star
    for star in soup.select('div.shopee-rating-stars__star-wrapper > div.shopee-rating-stars__lit'):
        # print(star)
        # print(star['style'])
        _star = _star + float(star['style'].split(" ")[1].split("%")[0]) 

    _star = round(_star / 100,4)
    # print(_star)  

    #from
    __from = soup.select_one("div._2CWevj")
    if (__from):
        _from = __from.text
        # print(__from.get_text())

    # find img path
    imgs = soup.select_one("div._25_r8I._2SHkSu > img")
   
    try:
        _image = imgs['src']
        # print (imgs['src'])
    except:
        print('no image source')

    #url
    url = soup.select_one("a")
    item_url.append("https://shopee.co.th/"+url['href'])
    _url = "https://shopee.co.th/"+url['href']
    _id = (url['href']).split(".")[len((url['href']).split("."))-1]
    # print(_id)
    # print(url['href'])

    return {
        "name" : _name,
        "price" : _price,
        "sold": _sold,
        "from" :_from,
        "img_src":_image,
        "url" :_url,
        "type" : _type,
        "star" : _star,
        "id" : _id
    }
    


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
        _name = name.text
        # print(name.get_text())
        # print("no name")

    #item id
    item_code = soup['data-asin']
    if (item_code):
        _id = item_code
    
    # Price
    price = soup.select_one("span.a-price > span.a-offscreen")
    if (price):
        _price = float((price.text).split("$")[1])
        print(_price)

    # rating
    rating = soup.select_one("i > span.a-icon-alt")
    if (rating):
        _rating = float((rating.text).split(" ")[0])
        # print(rating.get_text())

    #review
    review = soup.select_one("a.a-link-normal > span.a-size-base")
    if (review):
        _review = review.text
        # print(review.get_text())

        
    imgs = soup.select_one("img.s-image")
    if (imgs):
        _image = imgs['src']
    # print(imgs['src'])

    #best?
    bestseller = soup.select_one("div.a-row.a-badge-region > span.a-badge > span.a-badge-label > span.a-badge-label-inner.a-text-ellipsis > span.a-badge-text ")
    # print(bestseller)
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


# #################################################################################################

def getItemDataForPantip(link):

    _title = "no title"
    _author = "no author"
    _author_id = "no author id"
    _story = "no story"
    _likecount = "no like"
    _emocount = "no emo"
    _allemos = "no emos"
    _tags = "no tags"
    _datetime = "no time"
    _post_link = "no link"
    _img_src = "no img"
    _post_id = "no post id"
    _meaning = "notthing"
    _good_words = []
    _bad_words = []
    pos = 0
    neg = 0

    start_page = requests.get(link)
    start_page.encoding = 'utf-8'
    
    tree = htmllxml.fromstring(start_page.text)

    _post_link = link
    _post_id = link.split("/")[4]
    _title = tree.xpath('//h2[@class="display-post-title"]/text()')[0]
    _author = tree.xpath('//a[@class="display-post-name owner"]/text()')[0]
    _author_id = tree.xpath('//a[@class="display-post-name owner"]/@id')[0]
    _story = tree.xpath('//div[@class="display-post-story"]')[0].text_content()
    words = custom_tokenizer.word_tokenize(_story)
    # print(words)
    
    for word in words:
        if word in positive_vocab:
            if word not in _good_words:
                pos = pos + 1
            else:
                pos = pos + 0.5
            _good_words.append(word)
            # print(word)
        if word in negative_vocab or word in swear_words:
            if word not in _bad_words:
                neg = neg + 1
            else:
                neg = neg + 0.5
            _bad_words.append(word)
            # print(word)

    if pos > neg:
        _meaning = 'positive'
        # print('positive')
    elif neg > pos:
        _meaning = "negative"
        # print('negative')
    else:
        _meaning = 'neutral'
        # print('neutral')



    _likecount = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
    _emocount = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
    _allemos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
    _tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item cs-tag_topic_title"]/text()')
    _datetime = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]
    _img = tree.xpath('//img[@class="img-in-post"]/@src')
    if (len(_img) > 0):
        # print(_img[0])
        _img_src = _img[0]

    return{
        "title" : _title,
        "author" : _author,
        "author_id" : _author_id,
        "story" : _story,
        "likeCount" :_likecount,
        "emocount" : _emocount,
        "allemos" : _allemos,
        "tags" : _tags,
        "dateTime" : _datetime,
        "post_link" : _post_link,
        "img_src" : _img_src,
        "post_id" : _post_id,
        "meaning" : _meaning,
        "goodWords" : _good_words,
        "badWords" : _bad_words

    }
    ###################################################################################
def getItemDataForJD(item):

    _name = 'no name'
    _price = 'no price'
    _image = 'no image'
    _from = 'no data'
    _id = 'no id'
    _review = "no review"
    _type = 'general'
    _url = "no url"

    # Get Name
    try:
        _name = item['wname']
    
    except:
        print("no name")

    try:
        _price = float(item['jdPrice'])
    except:
        print("no price")

    try:
        _image = item['imageurl']
    except:
        print("no img")

    try:
        _id = item['spuId']
    except:
        print("no id")
    
    try:
        _url = "https://www.jd.co.th/product/"+ _id +".html"
    except:
        print("no url")

    try:
        _type = item['shopName']
    except:
        print("no type")

    try:
        _review = int((item['reviews']).split(" ")[0])
    except:
        print("no review")
    
    try:
        _from = item['localDelivery']
    except:
        print("no from")
    

    return {
        "name" : _name,
        "id" : _id,
        "price" : _price,
        "img_src":_image,
        "type" : _type,
        "review" : _review,
        "from" : _from,
        "url" : _url
    }
    ##########################################################
def getItemDataForFacebook(post):
    _user_name = "no name"
    _comment = 0
    _date = "no time"
    _image_h = ""
    _image_l = ""
    _reactions = []
    _post_url = "no link"
    _post_id = "no post id"
    _post_text = "no text"
    _meaning = "nothing"
    _good_words = []
    _bad_words = []
    pos = 0
    neg = 0

    # print(post)
    # print('++++++++++++++++++++++++++++++++++++++++++++')
    _post_id = post['post_id']
    # print(_post_id)
    _post_text = post['post_text']


    #แยกคำ
    words = custom_tokenizer.word_tokenize(_post_text)
    #find word i array files
    for word in words:
        if word in positive_vocab:
            if word not in _good_words:
                pos = pos + 1
            else:
                pos = pos + 0.5
            _good_words.append(word)
            # print(word)
        if word in negative_vocab or word in swear_words:
            if word not in _bad_words:
                neg = neg + 1
            else:
                neg = neg + 0.5
            _bad_words.append(word)
            # print(word)

    if pos > neg:
        _meaning = 'positive'
        # print('positive')
    elif neg > pos:
        _meaning = "negative"
        # print('negative')
    else:
        _meaning = 'neutral'
        # print('neutral')
    
    try:
        # print(post)
        # print(_post_text)
        _date = post['time']
        # print(_date)
        _image_h = post['images'][0]
        # print(_image_h)
        _image_l = post['images_lowquality'][0]
        # print(_image_l)
        _reactions = post['likes']
        # print(post['likes'])
        _comment = post['comments']
        # print(_comment)
        _post_url = post['post_url']
        # print(_post_url)
        _user_name = post['username']
        # print(_user_name)

    except:
        print("error")
    

    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

    return{
        "user_name":_user_name,
        "comment":_comment,
        "date" :_date,
        "image_h" :_image_h,
        "image_l" :_image_l,
        "reaction":_reactions,
        "post_url":_post_url,
        "post_id" :_post_id,
        "post_text":_post_text,
        "goodWords" : _good_words,
        "badWords" : _bad_words,
        "meaning" : _meaning
    }



    ###########################################################
def getItemDataForBedo(item):
    _group = "no group"
    _thai_name = "no thai name"
    data ={}
 
    # print(item.select_one("div.title").text)
    if ("กลุ่มทรัพยากรชีวภาพ" in item.select_one("div.title").text):
        _group = item.select_one("div.value").text

    if ("ชื่อพันธุ์ไทย" in item.select_one("div.title").text):
        _thai_name = item.select_one("div.value").text
    else:
        print("else")


    return {
        "group" : _group,
        "thai_name" : _thai_name
    }
    

#############################################
# shopee set
if(ss == 1):
    base_url = "https://shopee.co.th/search?keyword=" + keyword
    header_field = ["num","name","price","type","star","sold","from","img_src","url","id"]
    page=0
    csv.setHeader(header_field)

    while page<page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            print ("Page is ready")
            print("on page %d of %d" % (page+1,page_count))
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
    base_url = "https://www.amazon.com/s?k=" + keyword
    header_field = ["num","id","name","price","rating","review","img_src","url","rank"]
    page=1
    csv.setHeader(header_field)
    
    while page<=page_count:
        try:
            browser.get(base_url + "&page=" +str(page))
            WebDriverWait(browser, delay)
            print ("Page is ready")
            print("on page %d of %d" % (page,page_count))
            
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

#pantip
elif (ss == 3):
    base_url = "https://pantip.com/search?q=" + keyword
    header_field = ["num","title","author","author_id","story","likeCount","emocount","allemos","tags","dateTime","post_link","img_src","post_id","meaning","goodWords","badWords"]
    csv.setHeader(header_field)
    browser.get(base_url)
    WebDriverWait(browser, delay)
    browser.execute_script("window.scrollTo(0, 0);")

    #sort search click
    browser.execute_script("document.getElementById('timebias_2').checked = true")
    browser.execute_script("document.getElementById('searchbutton').click()")
    sleep(5)

    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    sort = soup.select_one('div.pt-lists-item__form.pure-material-radio.m-t-2 > input')

    print ("Page is ready")
    sleep(5)
    getDataFormPostForPantip(html)
    csv.addDataForPantip(products)

#JD
elif(ss == 4):
    page=1
    header_field = ["num","name","id","price","img_src","type","review","from","url"]
    
    csv.setHeader(header_field)

    while page<=page_count:
        try:
            base_url = ("https://api.jd.co.th/client.action?body={'pagesize':'60','page':'" + str(page) +"','keyword':'" + keyword + "'}&functionId=search&client=pc&clientVersion=2.0.0&lang=th_TH&area=184549376-185008128-185008132-0")
            browser.get(base_url)
            WebDriverWait(browser, delay)
            print ("Page is ready")
            print("on page %d of %d" % (page,page_count))
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
          
           # print(html)
            getDataFromPostForJD(html)
            page+=1
                        
             # it will break from the loop once the specific element will be present. 
        except TimeoutException:
            print ("Loading took too much time!-Try again")

    csv.addDataForJD(products)

elif (ss ==5):
    header_field = ["num","user_name","comment","date","image_h","image_l","reaction","post_url","post_id","post_text","meaning","goodWords","badWords"]
    
    csv.setHeader(header_field)
    try:
        getDataFromPostForFacebook(keyword,page_count)
        

    except TimeoutException:
            print ("Loading took too much time!-Try again")

    csv.addDataForFacebook(products)

elif(ss == 6):
    page = 1
    # header_field = ["bio_Group","number","group","thai_name","rev_amount","flowering_day","seeding",]
    header_field = ["num","group","thai_name"]

    csv.setHeader(header_field)
    
    while page <= page_count:
        try:
            base_url = ("https://www.thaibiodiversity.org/bedo/bioDetail/" + str(page))
            browser.get(base_url)
            WebDriverWait(browser,delay)
            print ("Page is ready")
            print("on page %d of %d" % (page,page_count))
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            print("get DATA BEDO")
            getDataFromPostForBedo(html)

            page = page+1

        except TimeoutException:
            print ("Loading took too much time!-Try again")
    csv.addDataForBedo(products)


browser.close()
print("End process")




