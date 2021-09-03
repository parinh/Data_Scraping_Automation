import csv
from decouple import config
from decouple import config
import requests
import logging

class Thaijo:
    def __init__(self):
        self.datas = []
        self.csv_count = 0

    def getItem(self,response):
        research = []
        _abstract_clean = "no abstract"
        _title = "no title"
        _article_url = "no url"
        _issue_date_published = "no date published"
        _issue_cover_image = "no img"
        _authors_full_name = "no author name"
        _authors_affiliation = "no affiliation"
        _issue_id = "no id"

        try:
            # print(response.json().get("result")[0])
            try:
                abstract_clean = response.get("abstract_clean").get('th_TH')
                if(abstract_clean):
                    _abstract_clean = abstract_clean
            except Exception:
                pass
        
            try:
                title =response.get("title").get('th_TH')
                if(title):
                    _title=title
            except Exception:
                pass

            try:                
                article_url =response.get("articleUrl")
                if(article_url):
                    _article_url = article_url
            except Exception:
                pass
        
            try:
                issue_date_published=response.get("issueDatePublished")
                if(issue_date_published):
                    _issue_date_published=issue_date_published
            except Exception:
                pass
            
            try:
                issue_cover_image=response.get("issue_cover_image")
                if(issue_cover_image):
                    _issue_cover_image=issue_cover_image
                else:
                    issue_cover_image=response.get("issueCoverImage").get("th_TH")
                    if(issue_cover_image):
                        _issue_cover_image=issue_cover_image
                    else:
                        issue_cover_image=response.get("issueCoverImage").get("en_US")
                        if(issue_cover_image):
                            _issue_cover_image=issue_cover_image

            except Exception:
                pass

            try:
                authors_full_name = response.get("authors")[0].get("full_name").get("th_TH")
                if(authors_full_name):
                    _authors_full_name = authors_full_name
            except Exception:
                pass

            try:
                authors_affiliation = response.get("authors")[0].get("affiliation").get("th_TH")
                if(authors_affiliation):
                    _authors_affiliation = authors_affiliation
            except Exception:
                pass

            issue_id=response.get("issue_id")
            if(issue_id):
                _issue_id=issue_id

            

            research = {
                "issue_id":_issue_id,
                "title": _title,
                "abstract_clean":_abstract_clean,
                "article_url":_article_url,
                "issue_date_published":_issue_date_published,
                "issue_cover_image":_issue_cover_image,
                "authors_full_name":_authors_full_name,
                "authors_affiliation":_authors_affiliation
            }
        

            # print(research)

            return research

        except Exception as e:
            print("get item error")
            print(e)

            

        

    def getData (self,keyword,page):
        try:
            # print(page)
            # print(keyword)
            query = {"term":keyword,"page":page,"size":1,"strict":True,"title":True,"author":True,"abstract":True}
            response = requests.post('https://www.tci-thaijo.org/api/articles/search/', json=query)
            # print(response.text)
            result = response.json().get("result")[0]
            logging.info(result)
            # print(result)

            # if(result == "list index out of range"):
            #     page = 1000
            #     return(page)
            # else:
            self.datas.append(self.getItem(result))

            return(page)

            # print(result)
            # print("\n")
            # self.getItem(response)
        except Exception as e:
            print("error getData")
            print(e)    
            logging.warning(e)  
            page = 1000
            return(page)    


    def toCsv (self,datas):
        try:
            with open(config("FILE"), "w", encoding="utf-8", newline="") as csvfile:
                head_csv = ["num","issue_id","title","abstract_clean","article_url","issue_date_published",
                "issue_cover_image", "authors_full_name", "authors_affiliation"]
                thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
                thewriter.writeheader()
                for i in range(len(datas)):
                 
                    self.csv_count += 1
                    thewriter.writerow(
                        {
                            "num": self.csv_count,
                            "issue_id": datas[i]["issue_id"],
                            "title": datas[i]["title"],
                            "abstract_clean": datas[i]["abstract_clean"],
                            "article_url": datas[i]["article_url"],
                            "issue_date_published": datas[i]["issue_date_published"],
                            "issue_cover_image": datas[i]["issue_cover_image"], 
                            "authors_full_name": datas[i]["authors_full_name"], 
                            "authors_affiliation": datas[i]["authors_affiliation"]
                        }
                    )
        except Exception:
            pass
            

