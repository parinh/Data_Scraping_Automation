from nlp import NLP
from facebook_scraper import *
from datetime import datetime
import csv

from requests.api import options


class Facebook:
    def __init__(self):
        self.csv_count =0
        self.posts =[]

    def getPosts(self,page_id,page_count):
        
        for post in get_posts(account=page_id,pages = page_count, page_limit = 100,timeout = 10,options = {"posts_per_page": 10}):
            nlp = NLP()
            nlp.check(post['text'])
            post.update({'score' : nlp.check_words[0]})
            post.update({'polarity' : nlp.check_words[1]})
            self.posts.append(post)
            
            
        
    def toCsv(self,posts):
        with open('csv/facebook-posts.csv','w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","text","score","polarity","like","comment","shared","date_time","img_src","url"]
            sorted_posts = sorted(posts,key=lambda x:x['time'],reverse = True)
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(posts)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "id": sorted_posts[i]['post_id'],
                        "text": sorted_posts[i]['text'],
                        "score": sorted_posts[i]['score'],
                        "polarity": sorted_posts[i]['polarity'],
                        "like": sorted_posts[i]['likes'],
                        "comment": sorted_posts[i]['comments'],
                        "shared": sorted_posts[i]['shares'],
                        "date_time": sorted_posts[i]['time'],
                        "img_src":sorted_posts[i]['image'],
                        "url":sorted_posts[i]['w3_fb_url']
                    }
                )