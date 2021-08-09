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
        post = []
        _abstract_clean = "noting"
        _title = "noting"
        _article_url = "noting"
        _issue_date_published = "noting"
        _issue_cover_image = "noting"
        _authors_full_name = "noting"
        _authors_affiliation = "noting"
        _issue_date = "noting"
        _issue_id = ""

        _abstract_clean = response.json().get("result")[0].get("abstract_clean").get('th_TH')
        _title=response.json().get("result")[0].get("title").get('th_TH')
        # print(_title)
        _article_url =response.json().get("result")[0].get("articleUrl")
        _issue_date_published=response.json().get("result")[0].get("issueDatePublished")
        _issue_cover_image=response.json().get("result")[0].get("issueCoverImage").get("en_US")
        _authors_full_name = response.json().get("result")[0].get("authors")[0].get("full_name").get("th_TH")
        _authors_affiliation = response.json().get("result")[0].get("authors")[0].get("affiliation").get("th_TH")
        _issue_id=response.json().get("result")[0].get("issue_id")

        print(_abstract_clean)
        print(_title)
        print(_article_url)
        print(_issue_date_published)
        print(_issue_cover_image)
        print(_authors_affiliation)
        print(_authors_full_name)
        print(_issue_id)
        print("\n")


        post = {
            "title": _title,
            

        }

        return post

        

    def getData (self,keyword,page):
        query = {"term":keyword,"page":page,"size":1,"strict":True,"title":True,"author":True,"abstract":True}
        response = requests.post('https://www.tci-thaijo.org/api/articles/search/', json=query)
        self.getItem(response)
        self.posts.append(self.getItem(response))

    def toCsv (self,datas):
        with open(config("THAIJO_FILE"), "a", encoding="utf-8", newline="") as csvfile:
            head_csv = ["num","group","name"]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(datas)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "group": datas[i]["group"],
                        "name": datas[i]["name"]
                    }
                )

