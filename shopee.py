from os import name
from bs4 import BeautifulSoup
import csv
import tocsv
from decouple import config
from numpy import product
from decouple import config


class Shopee:
    def __init__(self):
        self.csv_count = 0
        self.products = []

    # get item
    def getItem(self, soup):
        product = []
        _name = "no name"
        _price = 0
        _sold = "no sold"
        _from = "no from"
        _image = "no image"
        _url = "no url"
        _type = "general"
        _star = 0
        _id = "no id"

        # Name
        name = soup.select_one("div._1nHzH4 > div.PFM7lj > div.yQmmFK._1POlWt._36CEnF")
        if name:
            _name = name.text
        # Price
        price = soup.select_one("div.WTFwws._1lK1eK._5W0f35")
        if price:
            _price = float("".join((price.text).split(" ")[0].split("฿")[1].split(",")))
        # type
        __type = soup.select_one("div.Oi0pcf.KRP-a_ > span._2_d9RP")
        if __type:
            _type = __type.text
        __type = soup.select_one("div._1qt0vU > div.Oi0pcf._3Bekkv")
        if __type:
            _type = "shopee mall"
        # sold / month
        sold = soup.select_one("div.go5yPW")
        if sold.text:
            if "พัน" not in sold.text:
                _sold = float((sold.text).split(" ")[1])
            else:
                _sold = float((sold.text).split(" ")[1].split("พัน")[0]) * 1000
        # star
        for star in soup.select(
            "div.shopee-rating-stars__star-wrapper > div.shopee-rating-stars__lit"
        ):
            _star = _star + float(star["style"].split(" ")[1].split("%")[0])
        _star = round(_star / 100, 4)
        # from
        __from = soup.select_one("div._2CWevj")
        if __from:
            _from = __from.text
        # find img path
        imgs = soup.select_one("div._25_r8I._2SHkSu > img")
        try:
            _image = imgs["src"]
        except:
            _image = "no image"
        # url
        url = soup.select_one("a")
        _url = "https://shopee.co.th/" + url["href"]
        # product_id
        _id = (url["href"]).split(".")[len((url["href"]).split(".")) - 1]

        product = {
            "name": _name,
            "price": _price,
            "sold": _sold,
            "from": _from,
            "img_src": _image,
            "url": _url,
            "type": _type,
            "star": _star,
            "product_id": _id
        }
        return product

    def getData(self, html):
        soup = BeautifulSoup(html, "html.parser")
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
