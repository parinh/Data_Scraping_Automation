from bs4 import BeautifulSoup
from lxml import html
import json
import requests
from requests.api import post
from requests.exceptions import ConnectionError, ReadTimeout
import csv
from datetime import datetime
from nlp import *
from decouple import config

class Pantip:

    def __init__(self) :
        self.csv_count = 0
        self.posts = []
        # self.nlp = NLP()

    def getPosts(self,html,page_count,browser):
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
        for post in soup.select('div.rowsearch.card.px-0 > div.desc.col-md-12 > a.datasearch-in'): 
            # post_url = post.select_one("div.rowsearch.card.px-0 > div.title.col-md-12 > a.datasearch-in")
            self.posts.append(self.getItem(post['href']))


    def getItem(self,link):
        nlp = NLP()
        post = {}
        _title = "no title"
        _author = "no author"
        _author_id = "no author id"
        _story = "no story"
        _likecount = "no like"
        _emocount = "no emo"
        _allemos = "no emos"
        _tags = "no tags"
        _datetime = "no time"
        _post_link = link
        _img_src = "no img"
        _post_id = "no post id"
        _meaning = "no thing"
        start_page = requests.get(link)
        start_page.encoding = 'utf-8'
        tree = html.fromstring(start_page.text)

        _post_link = link
        # print(_post_link)
        _post_id = link.split("/")[len(link.split("/"))-1]
        _title = tree.xpath('//h2[@class="display-post-title"]/text()')[0]
        _story = tree.xpath('//div[@class="display-post-story"]')[0].text_content()
        nlp.check(_story)
        _author = tree.xpath('//a[@class="display-post-name owner"]/text()')[0]
        _author_id = tree.xpath('//a[@class="display-post-name owner"]/@id')[0]
        _likecount = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
        _emocount = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
        _allemos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
        _tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item"]/text()')
        _datetime = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]

        img = tree.xpath('//img[@class="img-in-post"]/@src')
        if (len(img) > 0):
            _img_src = img[0]

        post = {
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
            "meaning" : nlp.check_words[1],
            "good_words" : nlp.check_words[2],
            "bad_words" : nlp.check_words[3]
        }
        return post

    def toCsv(self,posts):
        with open(config("FILE"), 'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","title","author","author_id","story","like_count","emo_count","allemos","tags","date_time","post_link","img_src","post_id","meaning","good_word","bad_word"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()
            for i in range(len(posts)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "title" : posts[i]['title'],
                        "author" : posts[i]['author'],
                        "author_id": posts[i]['author_id'],
                        "story" :posts[i]['story'],
                        "like_count":posts[i]['likeCount'],
                        "emo_count" :posts[i]['emocount'],
                        "allemos" : posts[i]['allemos'],
                        "tags" : posts[i]['tags'],
                        "date_time" : posts[i]['dateTime'],
                        "post_link" : posts[i]['post_link'],
                        "img_src" : posts[i]['img_src'],
                        "post_id" : posts[i]['post_id'],
                        "meaning" : posts[i]['meaning'],
                        "good_word" : posts[i]['good_words'],
                        "bad_word" : posts[i]['bad_words']
                    }
                )
        
        
    
            
    
