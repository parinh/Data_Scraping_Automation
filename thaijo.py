from os import name
from bs4 import BeautifulSoup
import csv
import tocsv
from decouple import config
from numpy import product
from decouple import config
import requests

class Thaijo:
    def __init__(self):
        self.posts = []

    def getItem(self,response):
        posts = []
        _abstract_clean = "noting"
        _title = "noting"
        _articleUrl = "noting"
        _issueDatePublished = "noting"
        _issueCoverImage = "noting"
        _authors_full_name = "noting"
        _authors_affiliation = "noting"
        _issus_date = "noting"

        # _abstract_clean = response.json().get("result")[0].get("abstract_clean").get('th_TH')
        _title=response.json().get("result")[0].get("title").get('th_TH')
        print(_title)
        # response.json().get("result")[0].get("articleUrl"))
        # response.json().get("result")[0].get("issueDatePublished"))
        # response.json().get("result")[0].get("issueCoverImage").get("en_US"))
        # response.json().get("result")[0].get("authors")[0].get("full_name").get("th_TH"))
        # response.json().get("result")[0].get("authors")[0].get("affiliation").get("th_TH"))
        # response.json().get("result")[0].get("issue_id"))

        # self.posts.append

    def getData (self,keyword,page):
        query = {"term":keyword,"page":page,"size":1,"strict":True,"title":True,"author":True,"abstract":True}
        response = requests.post('https://www.tci-thaijo.org/api/articles/search/', json=query)
        self.getItem(response)
