from facebook_scraper import *
from datetime import datetime
import csv

from requests.api import options


class Facebook:
    def __init__(self):
        self.csv_count =0
        self.posts =[]

    def getPosts(self,page_id,page_count):
        for post in get_posts(account=page_id,pages=2,page_limit=10,options={"posts_per_page":page_count}):
            self.posts.append(post)

            
        
    def toCsv(self,posts):
        with open('csv/facebook-posts.csv','w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","text","like","comment","shared","date_time","img_src","url"]
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
                        "like": sorted_posts[i]['likes'],
                        "comment": sorted_posts[i]['comments'],
                        "shared": sorted_posts[i]['shares'],
                        "date_time": sorted_posts[i]['time'],
                        "img_src":sorted_posts[i]['image'],
                        "url":sorted_posts[i]['w3_fb_url']
                    }
                )