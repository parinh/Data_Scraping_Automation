from numpy import log
from sciencedirect import ScienceDirect
from thaibio import ThaiBio
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from shopee import *
from facebook_scraper import *
from nlp import NLP
from amazon import *
from pantip import *
from tocsv import *
from jd import *
from facebook import *
from thaibio import *
from api_bedo import *
from pythainlp.corpus.common import thai_words
from pythainlp import *
from decouple import config
from thaijo import *
import requests
import logging
import csv
import math

# print(config("LOG_FILE"))
logging.basicConfig(filename=config("LOG_FILE"), filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# def printArr2D(arr):
#     for i in arr:
#         for j in i:
#             print(j)
#         print("##########")


# def printArr(arr):
#     for i in arr:
#         print(i)


# set
delay = 5
chrome_options = Options()
shopee = Shopee()
amazon = Amazon()
pantip = Pantip()
jd = JD()
facebook = Facebook()
thaijo = Thaijo()
thai_bio = ThaiBio()
science_direct = ScienceDirect()
nlp = NLP()
shopee_detail = Shopee()
chromedriver_path = config("CHROMEDRIVER")


# input
print(
    "select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = pantip][4 = JD][5 = FaceBook][6 = thaibio][7 = sciencedirect][8 = thaijo][9 = shopee detail][10 = amazon detail]->>"
)
ss = int(input())

if( ss < 9 ):
    print("enter number of pages//posts")
    page_count = int(input())

    print("Enter the keyword for the selected site.. ->>")
    keyword = input()

if(ss == 5):
    print("enter lasted post_id")
    lasted_post_id = input()
# close all popup
chrome_options.add_argument("disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")

# # Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)
# # chrome driv ja
browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
# for shopee
if ss == 1:
    base_url = "https://shopee.co.th/search?keyword=" + keyword
    page = 0
    count = 0
    last_results = 0
    page_count = page_count - 1
    while page <= page_count:
        try:
            browser.get(base_url + "&page=" + str(page))
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 1);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 2);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 3);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 4);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 5);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 6);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 7);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 8);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 9);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 10);"
            )
            sleep(5)
            html = browser.execute_script(
                "return document.getElementsByTagName('html')[0].innerHTML"
            )
            results = shopee.getData(html)
            if(results == last_results):
                count += 1
                # print(count)
            else:
                # print("enter else")
                last_results = results
                count = 0
                # print(count)

            if (count >= 3):
                break
            page += 1

        except TimeoutException:
            print("Loading took too much time!-Try again")

    shopee.toCsv(shopee.products)
    # printArr(shopee.products)

# for amazon search
elif ss == 2:
    base_url = "https://www.amazon.com/s?k=" + keyword
    page = 1
    count = 0
    last_results = 0
    while page <= page_count:
        try:
            browser.get(base_url + "&page=" + str(page))
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 1);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 2);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 3);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 4);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 5);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 6);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 7);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 8);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 9);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 10);"
            )
            sleep(5)
            html = browser.execute_script(
                "return document.getElementsByTagName('html')[0].innerHTML"
            )
            results = amazon.getData(html)
            # print(results)
            if(results == last_results):
                count += 1
                # print(count)
            else:
                # print("enter else")
                last_results = results
                count = 0
                # print(count)

            if (count >= 3):
                break

            page += 1

        except TimeoutException:
            print("Loading took too much time!-Try again")

    amazon.toCsv(amazon.products)


# pantip
elif ss == 3:
    try:
        base_url = "https://pantip.com/search?q=" + keyword
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

        pantip.getPosts(html,page_count,browser)
        # printArr(pantip.posts)
        pantip.toCsv(pantip.posts)
    except Exception as e:
        logging.warning(e)
        
# JD
elif ss == 4:
    page = 1
    count = 0
    last_results = 0
    
    while page <= page_count:
        try:
            base_url = (
            "https://api.jd.co.th/client.action?body={'pagesize':'60','page':'"
            + str(page)
            + "','keyword':'"
            + keyword
            + "'}&functionId=search&client=pc&clientVersion=2.0.0&lang=th_TH&area=184549376-185008128-185008132-0"
            )
            browser.get(base_url)
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 1);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 2);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 3);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 4);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 5);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 6);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 7);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 8);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 9);"
            )
            browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 10);"
            )
            sleep(5)
            html = browser.execute_script(
                "return document.getElementsByTagName('html')[0].innerHTML"
            )     
            results = jd.getProducts(html)
            if(results == last_results):
                count += 1
                # print(count)
            else:
                # print("enter else")
                last_results = results
                count = 0
                # print(count)

            if (count >= 3):
                break

            page += 1

        except TimeoutException:
            print("Loading took too much time!-Try again")

    jd.toCsv(jd.products)

# facebook
elif ss == 5:
    print(lasted_post_id)
    if page_count <= 100:
        facebook.getPosts(keyword, page_count,lasted_post_id)
    else:
        print("cant get posts // pages limit was set on 100 ")

    facebook.toCsv(facebook.posts)

# thai_bio
elif ss == 6:
    page = 1+5366
    while page <= page_count:
        try:
            base_url = ("https://thaibiodiversity.org/bedo/bioDetail/"+str(page))
            browser.get(base_url)
            WebDriverWait(browser, delay)
            sleep(5)
            browser.execute_script("window.scrollTo(0, 0);")
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            print(page)
            thai_bio.getData(html)
            page += 1
        except:
            print("error thai bio")
            break

    thai_bio.toCsv(thai_bio.datas)

# science_direct
elif ss == 7:
    page = 0
    try:
        # base_url = ("https://www.sciencedirect.com/search/api?qs=chicken&t=ZNS1ixW4GGlMjTKbRHccgcML%252BaxSRKhvfLPhn5%252FngR7q2yS0Xo9jYGehwK6EP%252BXLBQmO3M1qEYx%252FhyQ9F73W6aWzCL7gRpIEXR39JSVyCujf6EajB%252BYREjbhdYoZjlowvKdDbfVcomCzYflUlyb3MA%253D%253D&hostname=www.sciencedirect.com")
        base_url = ("https://www.sciencedirect.com/search?qs="+str(keyword))
        browser.get(base_url)
        WebDriverWait(browser, delay)
        sleep(5)
        browser.execute_script("window.scrollTo(0, 0);")
        browser.execute_script(
            "window.scrollTo(0, (document.body.scrollHeight /10) * 1);"
        )
        sleep(3)
        try:
            browser.execute_script("document.querySelector('.button-link.facet-link-container.u-font-sans.button-link-primary').click()")
            print("clikced")
        except:
            print("not clicked")
        # browser.execute_script(
        #     "window.scrollTo(0, (document.body.scrollHeight /10) * 2);"
        # )
        # sleep(5)
        html = browser.execute_script(
                "return document.getElementsByTagName('html')[0].innerHTML"
            ) 
        science_direct.getData(html)
        # print(1)
        science_direct.toCsv(science_direct.datas,keyword)
        print(2)
        # science_direct.sum(science_direct.datas)
        
        
    except Exception as e:
        print(e)

# thaijo
elif ss == 8:
    try:
        page = 1
        keyword_input = open(config("INPUT_FILE_TXT"),"r",encoding = "utf8").read()
        print(keyword_input)

    except Exception as e:
        logging.warning("read")
        logging.warning(e)
    
    while page <= page_count:
        try:
            
            total = thaijo.getData(keyword_input,page)
            page_count = math.ceil(total/30)
            print(page_count)

            # print(thaijo.datas)
        except Exception as e:
            logging.warning(e)
            page = 1000
            page_count = 0
        page += 1
    
    thaijo.toCsv(thaijo.datas)

# shopee detail
elif ss == 9:
    with open(config("INPUT_FILE_CSV"),'r',encoding='utf-8') as f:
        datas = csv.reader(f)
        next(datas)
        count = 0
        for row in datas:
            try:
                count += 1
                base_url = row[1]
                browser.get(base_url)
                WebDriverWait(browser, delay)
                sleep(3)
                browser.execute_script("window.scrollTo(0, 0);")
                browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 1);")
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 2);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 3);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 4);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 5);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 6);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 7);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 8);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 9);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 10);"
                )
                html = browser.execute_script(
                    "return document.getElementsByTagName('html')[0].innerHTML"
                )
                shopee_detail.getDetail(row[0],html)
            except Exception as e:
                print(e)
                pass
        shopee_detail.detailToCsv(shopee_detail.details)
        # print(shopee_detail.details)

# amazon detail
elif ss == 10:
    with open(config("INPUT_FILE_CSV"),'r',encoding='utf-8') as f:
        datas = csv.reader(f)
        next(datas)
        count = 0
        for row in datas:
            try:
                count += 1
                base_url = row[1]
                count += 1
                browser.get(base_url)
                WebDriverWait(browser, delay)
                sleep(3)
                browser.execute_script("window.scrollTo(0, 0);")
                browser.execute_script(
                "window.scrollTo(0, (document.body.scrollHeight /10) * 1);")
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 2);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 3);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 4);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 5);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 6);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 7);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 8);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 9);"
                )
                browser.execute_script(
                    "window.scrollTo(0, (document.body.scrollHeight /10) * 10);"
                )
                html = browser.execute_script(
                    "return document.getElementsByTagName('html')[0].innerHTML"
                )
                amazon.getDetail(row[0],html)
                
            except Exception as e:
                print(e)
                pass
    amazon.detailToCsv(amazon.details)

elif ss == 11:
    try:
        types = ['plants','animals','micros']
        for type in types:
            api_bedo = ApiBedo()
            filename = ""
            if type == "animals":
                filename = "ANIMALS_BEDO"
            elif type == "micros":
                filename = "MICROS_BEDO"
            elif type == "plants":
                filename = "PLANTS_BEDO"

            auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9sb2NhbGhvc3QiLCJhdWQiOiJodHRwOlwvXC9sb2NhbGhvc3QiLCJpYXQiOjE2MzA2NDAyNTYsIm5iZiI6MTYzMDY0MDI1NiwiZXhwIjoxNjMzMjMyMjU2LCJ1aWQiOiJiZWRvX2FpIn0.gFfMgIjhcZ7qyeWzVXOduutGBmSD0T_BBRTFe0rHnmQ'
            i = 1
            while True:
                response = requests.get('http://api.bedo.or.th/api/v1/'+ type +'?page='+ str(i) +'&size=50',headers={'Authorization': 'Bearer ' + auth_token})
                results = response.json().get("data").get("items")        
                if(results == []):
                    break
                else:
                    api_bedo.getData(results)
                i+=1

            print(api_bedo.datas)
            api_bedo.toCsv(api_bedo.datas,filename)
                  
    except Exception as e:
        print(e)

        
browser.close()
print("End process")
