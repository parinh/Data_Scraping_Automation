from nlp import NLP
from facebook_scraper import *
from datetime import datetime
import csv
from decouple import config
from requests.api import options


class Facebook:
    def __init__(self):
        self.csv_count =0
        self.posts =[]

    def getPosts(self,page_id,page_count):
        for post in get_posts(account=page_id,pages = page_count, page_limit = 100,timeout = 10,options = {"posts_per_page": 10}):
           
            print(post['post_id'])
            self.posts.append(self.getData(post))

    def getData(self,post):
        nlp = NLP()
        _user_name = "no name"
        _comment = 0
        _date = "no time"
        _image_h = "no img"
        _image_l = "no img"
        _reactions = []
        _post_url = "no link"
        _post_id = "no post id"
        _post_text = "no text"
        _meaning = "nothing"
        _good_words = []
        _bad_words = []
       
        try:
            _post_id = post['post_id']
        except:
            print("no id")
        try:
            _post_text = post['post_text']
        except:
            print("no text")
        try:
            _date = post['time']
        except:
            print("no date")
        try:
            _image_h = post['images'][0]
        except:
            print("no img")
        try:
            _image_l = post['images_lowquality'][0]
        except:
            print("no img")
        try:
            _reactions = post['likes']
        except:
            print("no like")
        try:
            _comment = post['comments']
        except:
            print("no comment")
        try:
            _post_url = post['post_url']
            print(_post_url)
        except:
            print("no url")
        try:
            _user_name = post['username']
        except:
            print("no username")

        nlp.check(post['post_text'])
        _meaning = nlp.check_words[1]
        _good_words =nlp.check_words[2]
        _bad_words = nlp.check_words[3]
       

        face_post = {
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

        return face_post

        
    def toCsv(self,posts):
        with open(config("FILE"),'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","user_name","comment","date","image_h","image_l","reaction","post_url","post_id","post_text","meaning","good_word","bad_word"]
            # sorted_posts = sorted(posts,key=lambda x:x['date'],reverse = True)
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()
            for i in range(len(posts)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "user_name" : posts[i]['user_name'],
                        "comment" : posts[i]['comment'],
                        "date" : posts[i]['date'],
                        "image_h" : posts[i]['image_h'],
                        "image_l":posts[i]['image_l'],
                        "reaction" :posts[i]['reaction'],
                        "post_url" : posts[i]['post_url'],
                        "post_id" : posts[i]['post_id'],
                        "post_text" : posts[i]['post_text'],
                        "meaning" : posts[i]['meaning'],
                        "good_word" : posts[i]['goodWords'],
                        "bad_word" : posts[i]['badWords']
                    }
                )