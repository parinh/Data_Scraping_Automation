from bs4 import BeautifulSoup
from lxml import html
import json
import requests
from requests.api import post
from requests.exceptions import ConnectionError, ReadTimeout
import csv


class Pantip:

    def __init__(self) :
        self.csv_count = 0
        self.posts = []

    def getPosts(self,soup):
        for post in soup.find_all('div',class_='rowsearch card px-0'):
            post_url = post.select_one("div.rowsearch.card.px-0 > div.title.col-md-12 > a.datasearch-in")
            
            self.posts.append(self.getItem(post_url['href']))

    # def getData(self,html):
    #     soup = BeautifulSoup(html, "html.parser") 
    #     ch = 0 
    

    #     while (page_count > len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')) ): 
    #         sh = browser.execute_script("return document.body.scrollHeight")
    #         browser.execute_script("window.scrollTo(0, %d);"% ch)
    #         ch += sh/3
    #         # print(len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')))
    #         html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    #         soup = BeautifulSoup(html, "html.parser")


    #     for item_n in soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'): 
    #         # print(sh)
    #         link = item_n['href']
    #         data = getItemDataForPantip(link)
    #         products.append(data)
    #         # print(type(ch))

    def getItem(self,link):
        post = []
        start_page = requests.get(link)
        start_page.encoding = 'utf-8'
        tree = html.fromstring(start_page.text)

        id = link.split("/")[len(link.split("/"))-1]
        post.append(id)

        title = tree.xpath('//h2[@class="display-post-title"]/text()')[0]
        post.append(title)

        description = tree.xpath('//div[@class="display-post-story"]')[0].text_content()
        post.append(description)

        author = tree.xpath('//a[@class="display-post-name owner"]/text()')[0]
        post.append(author)

        # author_id = tree.xpath('//a[@class="display-post-name owner"]/@id')[0]
        # post.append(author_id)

        likeCount = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
        post.append(likeCount)

        emoCount = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
        post.append(emoCount)
        # allEmos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
        # post.append(allEmos)
        # tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item"]/text()')
        # post.append(tags)
        dateTime = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]
        post.append(dateTime)

        post.append(link)

        return post

    def toCsv(self,posts):
        with open('pantip-search.csv', 'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","title","description","author","like","emo","date-time","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(posts)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "id": posts[i][0],
                        "title": posts[i][1],
                        "description": posts[i][2],
                        "author": posts[i][3],
                        "like":posts[i][4],
                        "emo":posts[i][5],
                        "date-time":posts[i][6],
                        "url":posts[i][7]
                        
                    }
                )
        
        
# def getDataFormPostForPantip(html):
#     print ("get data Pantip")
#     soup = BeautifulSoup(html, "html.parser") 
#     ch = 0 
    

#     while (page_count > len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')) ): 
#         sh = browser.execute_script("return document.body.scrollHeight")
#         browser.execute_script("window.scrollTo(0, %d);"% ch)
#         ch += sh/3
#         # print(len(soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in')))
#         html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#         soup = BeautifulSoup(html, "html.parser")
    

#     for item_n in soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'): 
#         # print(sh)
#         link = item_n['href']
#         data = getItemDataForPantip(link)
#         products.append(data)
#         # print(type(ch))

    
#     def getItemDataForPantip(link):

#     _title = "no title"
#     _author = "no author"
#     _author_id = "no author id"
#     _story = "no story"
#     _likecount = "no like"
#     _emocount = "no emo"
#     _allemos = "no emos"
#     _tags = "no tags"
#     _datetime = "no time"
#     _post_link = "no link"
#     _img_src = "no img"

#     start_page = requests.get(link)
#     start_page.encoding = 'utf-8'

#     # print(start_page.text)
#     # print("##################################")
#     # print(htmllxml)

    
#     tree = htmllxml.fromstring(start_page.text)

#     _post_link = link
#     _title = tree.xpath('//h2[@class="display-post-title"]/text()')[0]
#     _author = tree.xpath('//a[@class="display-post-name owner"]/text()')[0]
#     _author_id = tree.xpath('//a[@class="display-post-name owner"]/@id')[0]
#     _story = tree.xpath('//div[@class="display-post-story"]')[0].text_content()
#     _likecount = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
#     _emocount = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
#     _allemos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
#     _tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item cs-tag_topic_title"]/text()')
#     print(_tags)
#     _datetime = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]
#     _img = tree.xpath('//img[@class="img-in-post"]/@src')
#     if (len(_img) > 0):
#         print(_img[0])
#         _img_src = _img[0]

#     return{
#         "title" : _title,
#         "author" : _author,
#         "author_id" : _author_id,
#         "story" : _story,
#         "likeCount" :_likecount,
#         "emocount" : _emocount,
#         "allemos" : _allemos,
#         "tags" : _tags,
#         "dateTime" : _datetime,
#         "post_link" : _post_link,
#         "img_src" : _img_src

#     }