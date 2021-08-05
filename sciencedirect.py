from os import name
from bs4 import BeautifulSoup
import csv
import tocsv
from decouple import config
from numpy import product
import requests

response = requests.get(r"https://www.sciencedirect.com/search/api?qs=chicken&t=ZNS1ixW4GGlMjTKbRHccgcML%252BaxSRKhvfLPhn5%252FngR7q2yS0Xo9jYGehwK6EP%252BXLBQmO3M1qEYx%252FhyQ9F73W6aWzCL7gRpIEXR39JSVyCujf6EajB%252BYREjbhdYoZjlowvKdDbfVcomCzYflUlyb3MA%253D%253D&hostname=www.sciencedirect.com")
print(response)


class ScienceDirect:
    def __init__(self):
        self.csv_count = 0
        self.products = []

    # get item
    def getItem(self, soup):
        product = []
        return product

    def getData(self, html):
        print("get data form shopee")
        soup = BeautifulSoup(html, "html.parser")
        for item_n in soup.select("div[data-sqe=item]"):
            if item_n.select_one("div.shopee-image-placeholder"):
                continue
            else:
                data = self.getItem(item_n)
                self.products.append(data)
        return(len(self.products))

    def toCsv(self, products):
        with open(config("FILE"), "w", encoding="utf-8", newline="") as csvfile:
            head_csv = [
                "num",
                "name",
                "price",
                "type",
                "star",
                "sold",
                "send_from",
                "img_src",
                "url",
                "product_id"
            ]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(products)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "name": products[i]["name"],
                        "price": products[i]["price"],
                        "sold": products[i]["sold"],
                        "star": products[i]["star"],
                        "send_from": products[i]["from"],
                        "img_src": products[i]["img_src"],
                        "url": products[i]["url"],
                        "type": products[i]["type"],
                        "product_id": products[i]["product_id"]
                    }
                )


#
