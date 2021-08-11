from os import name
from bs4 import BeautifulSoup
import csv
import tocsv
from decouple import config
from numpy import product
import requests

# response = requests.get(r"https://www.sciencedirect.com/search/api?qs=chicken&t=ZNS1ixW4GGlMjTKbRHccgcML%252BaxSRKhvfLPhn5%252FngR7q2yS0Xo9jYGehwK6EP%252BXLBQmO3M1qEYx%252FhyQ9F73W6aWzCL7gRpIEXR39JSVyCujf6EajB%252BYREjbhdYoZjlowvKdDbfVcomCzYflUlyb3MA%253D%253D&hostname=www.sciencedirect.com")
# print(response)


class ScienceDirect:
    def __init__(self):
        self.csv_count = 0
        self.datas = []

    def getData(self, html):
        print("get data from science")
        soup = BeautifulSoup(html, "html.parser")
        # > div.checkbox.checkbox-small.checkbox-label-indent > label.checkbox-label > span.checkbox-check.checkbox-small.checkbox-label-indent
        # for item in soup.select("div.FacetItem > fieldset.push-m > ol > li "):
        #     print(item.select_one("div.checkbox.checkbox-small.checkbox-label-indent > label.checkbox-label > span.checkbox-label-value.checkbox-small.checkbox-label-indent "))
        soup = soup.select_one("div.FacetItem > fieldset.push-m > ol")
        for item in soup.select("li > div.checkbox.checkbox-small.checkbox-label-indent > label.checkbox-label "):
            # > span.checkbox-label-value.checkbox-small.checkbox-label-indent 
            # print(item.select_one("div.checkbox.checkbox-small.checkbox-label-indent > label.checkbox-label > span.checkbox-label-value.checkbox-small.checkbox-label-indent "))
            # print(item)
            self.datas.append(self.getItem(item))
            # self.getItem(item)
    # get item
    def getItem(self, soup):
        count_in_year = []
        data=soup.select_one("span.checkbox-label-value.checkbox-small.checkbox-label-indent").text
        year=data.split(" ")[0]
        amount = float("".join(data.split(" ")[1].split("(")[1].split(")")[0].split(",")))
        count_in_year = {
            "year":year,
            "amount":amount
        }
        # print(count_in_year)
        return count_in_year

    def toCsv(self, datas,keyword):
        # filename = config("SCIENCE_DIRECT")+"-"+str(keyword)+".csv"
        with open(config("FILE"), "w", encoding="utf-8", newline="") as csvfile:
            head_csv = [
                "num",
                "year",
                "amount",
            ]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(datas)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "year": datas[i]["year"],
                        "amount": datas[i]["amount"],
                        
                    }
                )

    def sum(self,datas):
        a = sum(data.amount for data in datas)
        print(a)

#
