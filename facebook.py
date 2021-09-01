from nlp import NLP
from facebook_scraper import *
import csv
from decouple import config


class Facebook:
    def __init__(self):
        self.csv_count =0
        self.posts =[]

    def getPosts(self,page_id,page_count,lasted_post_id):
        for post in get_posts(account=page_id,pages = page_count, page_limit = 100,timeout = 10,options = {"posts_per_page": 10}):
            print(post['post_id'])
            if(post['post_id'] == lasted_post_id):
                print(post['post_id'])
                break            
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
        _food_words_count = 0
        _spa_words_count = 0
        _beauty_words_count = 0
        _travel_words_count = 0
        _health_words_count = 0
        _food_words=[]
        _spa_words=[]
        _beauty_words=[]
        _travel_words=[]
        _health_words=[]
       
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
        _meaning = nlp.check_words['meaning']
        _good_words =nlp.check_words['good_words']
        _bad_words = nlp.check_words['bad_words']
        _beauty_words_count = nlp.check_words['beauty_words_count']
        _food_words_count = nlp.check_words['food_words_count']
        _health_words_count = nlp.check_words['health_words_count']
        _spa_words_count = nlp.check_words['spa_words_count']
        _travel_words_count = nlp.check_words['travel_words_count']
        _food_words=nlp.check_words['food_words']
        _spa_words=nlp.check_words['spa_words']
        _beauty_words=nlp.check_words['beauty_words']
        _travel_words=nlp.check_words['travel_words']
        _health_words=nlp.check_words['health_words']

    

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
            "good_words" : _good_words,
            "bad_words" : _bad_words,
            "meaning" : _meaning,
            "food_words_count": _food_words_count,
            "health_words_count": _health_words_count,
            "beauty_words_count": _beauty_words_count,
            "spa_words_count":_spa_words_count,
            "travel_words_count":_travel_words_count,
            'food_words': _food_words,
            'health_words': _health_words,
            'beauty_words': _beauty_words,
            'spa_words': _spa_words,
            'travel_words': _travel_words,
        }
        nlp.clearCheckWord()

        return face_post

        
    def toCsv(self,posts):
        with open(config("FILE"),'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","user_name","comment","date","image_h","image_l","reaction","post_url","post_id","post_text","meaning","good_word","bad_word"
            ,"food_word_count","health_word_count","beauty_word_count","spa_word_count",
            "travel_word_count",'food_word','health_word','beauty_word','spa_word','travel_word']
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
                        "good_word" : posts[i]['good_words'],
                        "bad_word" : posts[i]['bad_words'],
                        "food_word_count": posts[i]['food_words_count'],
                        "health_word_count": posts[i]['health_words_count'],
                        "beauty_word_count": posts[i]['beauty_words_count'],
                        "spa_word_count": posts[i]['spa_words_count'],
                        "travel_word_count": posts[i]['travel_words_count'],
                        "food_word": posts[i]['food_words'],
                        "health_word": posts[i]['health_words'],
                        "beauty_word": posts[i]['beauty_words'],
                        "spa_word": posts[i]['spa_words'],
                        "travel_word": posts[i]['travel_words'],
                    }
                )