import csv
from bs4 import BeautifulSoup
from decouple import config
class ThaiBio :
    def __init__(self):
        self.datas = []

    def getData(self,html):
        soup = BeautifulSoup(html, "html.parser")
        # i = soup.select_one("div.bs-callout.bs-callout-info")
        # for item in soup.select("div[bs-callout bs-callout-info]"):

    def toCsv(self, products):
        with open(config("THAIBIO_FILE"), "w", encoding="utf-8", newline="") as csvfile:
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

        
