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
from lazada import *
from facebook import *
from thaibio import *
from pythainlp.corpus.common import thai_words
from pythainlp import *
from decouple import config
from thaijo import *
import requests


def printArr2D(arr):
    for i in arr:
        for j in i:
            print(j)
        print("##########")


def printArr(arr):
    for i in arr:
        print(i)


# set
delay = 5
chrome_options = Options()
shopee = Shopee()
amazon = Amazon()
pantip = Pantip()
lazada = Lazada()
jd = JD()
facebook = Facebook()
thaijo = Thaijo()
thai_bio = ThaiBio()
science_direct = ScienceDirect()
nlp = NLP()

chromedriver_path = config("CHROMEDRIVER")


# input
print(
    "select a number of site that need to scrapper.. [1 = shopee][2 = amazon-search][3 = pantip][4 = JD][5 = FaceBook][6 = thaibio][7 = sciencedirect][8 = thaijo]->>"
)
ss = int(input())

print("enter number of pages//posts")
page_count = int(input())

print("Enter the keyword for the selected site.. ->>")
keyword = input()
# close all popup
chrome_options.add_argument("disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")

# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)
# chrome driv ja
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
    

# elif ss == 3:
#     base_url = "https://pantip.com/search?q=" + keyword
#     browser.get(base_url)
#     ch = 0
#     count = 0
#     WebDriverWait(browser, delay)
#     browser.execute_script("window.scrollTo(0, 0);")
#     browser.execute_script("document.getElementById('timebias_2').checked = true")
#     browser.execute_script("document.getElementById('searchbutton').click()")
#     print("Page is ready")
#     sleep(5)
#     html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#     soup = BeautifulSoup(html, "html.parser")
#     sort = soup.select_one('div.pt-lists-item__form.pure-material-radio.m-t-2 > input')

#     while page_count > len(soup.select("div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in")):
#         current_len = len(soup.select("div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in"))
#         sh = browser.execute_script("return document.body.scrollHeight")
#         browser.execute_script("window.scrollTo(0, %d);" % ch)
#         ch += sh / 3

#         html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#         soup = BeautifulSoup(html, "html.parser")
#         if current_len == len(soup.select("div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in")):
#             count += 1
#             if count == 100:
#                 break
#         else:
#             count = 0

#         pantip.getPosts(soup)
#     pantip.toCsv(pantip.posts)


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
    if page_count <= 100:
        facebook.getPosts(keyword, page_count)
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
        browser.execute_script("document.querySelector('.button-link.facet-link-container.u-font-sans.button-link-primary').click()")
        # print(11111111)
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
    page = 1
    while page <= page_count:
        # try:
        thaijo.getData(keyword,page)
            # print(thaijo.datas)
        # except Exception as e:
        #     print(e)
        page += 1
        
    thaijo.toCsv(thaijo.datas)

browser.close()
print("End process")
