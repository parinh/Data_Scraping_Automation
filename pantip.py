from bs4 import BeautifulSoup
from lxml import html
import json
import requests
from requests.api import post
from requests.exceptions import ConnectionError, ReadTimeout
import csv
from datetime import datetime
from nlp import *

class Pantip:

    def __init__(self) :
        self.csv_count = 0
        self.posts = []

    def getPosts(self,soup):
        for post in soup.find_all('div',class_='rowsearch card px-0'):
            post_url = post.select_one("div.rowsearch.card.px-0 > div.title.col-md-12 > a.datasearch-in")
            self.posts.append(self.getItem(post_url['href']))


    def getItem(self,link):
        post = []
        title = "no title"
        author = "no author"
        description = "no story"
        date_time = "no time"
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

        like_count = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
        post.append(like_count)

        emo_count = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
        post.append(emo_count)
        # allEmos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
        # post.append(allEmos)
        # tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item"]/text()')
        # post.append(tags)
        date_time = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]
        post.append(date_time)

        img = tree.xpath('//img[@class="img-in-post"]/@src')
        if (len(img) > 0):
            img = img[0]
        else:
            img = "no image"

        post.append(img)
        post.append(link)

        return post

    def toCsv(self,posts):
        
        with open('csv/pantip-search.csv', 'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","title","description","author","like","emo","date-time","img","url"]
            posts.sort(key=lambda x: datetime.strptime(x[6], '%m/%d/%Y %H:%M:%S'),reverse = True)
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
                        "img":posts[i][7],
                        "url":posts[i][8]
                        
                    }
                )
        
        
    
            
    
