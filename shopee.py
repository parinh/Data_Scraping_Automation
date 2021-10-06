from ntpath import join
from os import name
from bs4 import BeautifulSoup
import csv
import tocsv
from decouple import config
from numpy import product
import logging



class Shopee:
    def __init__(self):
        self.csv_count = 0
        self.products = []
        self.details = []

    # get item
    def getItem(self, soup):
        product = []
        _name = "no name" 
        _price = 0
        _sold = 0
        _from = "no from"
        _image = "no image"
        _url = "no url"
        _type = "general"
        _star = 0
        _id = 0

        # a = soup.select_one("a > div > div > div:nth-child(2) > div:nth-child(1)")
        # print(a.text)
        # print(len(a))
        # print(a[1])
        # name = a[1].select_one("div")
        # print(name[0].select_one("div").text)
        try:
            # Name
            try:
                name = soup.select_one("a > div > div > div:nth-child(2) > div:nth-child(1)")
                if name:
                    _name = name.text
            except Exception as e:
                pass

            # Price
            try:
                price = soup.select_one("a > div > div > div:nth-child(2) > div:nth-child(2) > div > span:nth-child(2)")
                # print("".join(price.text.split(",")))
                if price:
                    _price = float("".join(price.text.split(",")))
            except Exception as e:
                pass

            # type
            try:
                selected = soup.select_one("a > div > div > div:nth-child(1)")
                __type = selected.find("div",attrs={"style":"color: rgb(242, 82, 32);"})
                if(__type):
                    _type = "ร้านแนะนำ"
                else:
                    __type = selected.find("div",attrs={"style":"color: rgb(208, 1, 27);"})
                    if(__type):
                        _type = "Mall"
                print(_type)
            except Exception as e:
                pass

            # sold / month
            try:
                sold = soup.select_one("a > div > div > div:nth-child(2) > div:nth-child(3) > div:nth-child(3)")
                if sold:
                    if "พัน" not in sold.text:
                        _sold = float((sold.text).split(" ")[1])
                    else:
                        _sold = float((sold.text).split(" ")[1].split("พัน")[0]) * 1000
                    print(_sold)
            except Exception as e:
                pass
            # print(_sold)

            # star
            try:
                for star in soup.select(
                    "div.shopee-rating-stars__star-wrapper > div.shopee-rating-stars__lit"
                ):
                    _star = _star + float(star["style"].split(" ")[1].split("%")[0])
                _star = round(_star / 100, 4)
            except Exception as e:
                pass

            # from
            try:
                __from = soup.select_one("a > div > div > div:nth-child(2) > div:nth-child(4)")
                if __from.text:
                    _from = __from.text
                print(_from)
            except Exception as e:
                pass
            # find img path

            #img src
            try:
                imgs = soup.select_one("div.customized-overlay-image > img")
                if imgs:
                    _image = imgs["src"]
            except Exception as e:
                pass
            # url
            url = soup.select_one("a")
            _url = "https://shopee.co.th" + url["href"]
            # product_id
            _id = int((url["href"]).split(".")[len((url["href"]).split(".")) - 1].split("?")[0])

        except Exception as e:
            print(e)
            print("something wrong")
            pass

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
        print("get data from shopee")
        soup = BeautifulSoup(html, "html.parser")
        for item_n in soup.select("div[data-sqe=item]"):
            if item_n.select_one("div.shopee-image-placeholder"):
                continue
            else:
                data = self.getItem(item_n)
                self.products.append(data)
        return(len(self.products))

    def getDetail(self,product_id,html):
        detail={}
        _rating = "no rating"
        _brand = "no brand"
        _description = "no description"
        _cat1 = "no cat1"
        _cat2 = "no cat2"
        _cat3 = "no cat3"
        soup = BeautifulSoup(html, "html.parser")
        soup = soup.select_one("div.page-product > div.container")

        #catagory
        try:
            _cat = soup.select_one("div")
            __cat1 = _cat.find_all("span")[0]
            if(__cat1):
                _cat1 = __cat1.text
            __cat2 = _cat.find_all("span")[1]
            if(__cat2):
                _cat2= __cat2.text
            __cat3 = _cat.find_all("span")[2]
            if(__cat3):
                _cat3 = __cat3.text
        except Exception as e:
            pass

            
        try:
            rating = ""
            rating = soup.select_one("div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div").text
            if(rating):
                if "พัน" in rating: 
                    _rating=float((rating).split("พัน")[0]) * 1000
                else:
                    _rating=float(rating)
        except Exception as e:
            logging.warning(e)
            pass
        
        try:
            brand = ""
            brand = soup.select_one("div:nth-child(3) > div._34c6X6.page-product__shop > div > div > div")
            if(brand):
                _brand=brand.text
        except Exception as e:
            logging.warning("brand")
            logging.warning(e)
            pass
        
        try:
            description = ""
            description = soup.select_one("div:nth-child(3) >div.page-product__content > div > div > div:nth-child(2) > div:nth-child(2)").text
            if(description):
                _description=description
        except Exception as e:
            logging.warning("descrip")
            logging.warning(e)
            pass
            
        detail = {
            'product_id':product_id,
            'rating': _rating,
            'brand': _brand,
            'description': _description,
            'cat1' : _cat1,
            'cat2' : _cat2,
            'cat3' : _cat3
        }
        self.details.append(detail)
        # print(product_id,rating,brand,description)

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

    def detailToCsv(self,details):
        with open(config("FILE"), "w", encoding="utf-8", newline="") as csvfile:
            head_csv = [
                "product_id",
                "brand",
                "rating",
                "description",
                "cat1",
                "cat2",
                "cat3"
            ]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(details)):
                thewriter.writerow(
                    {
                        "product_id": details[i]["product_id"],
                        "brand": details[i]["brand"],
                        "rating": details[i]["rating"],
                        "description": details[i]["description"],
                        "cat1" : details[i]["cat1"],
                        "cat2" : details[i]["cat2"],
                        "cat3" : details[i]["cat3"],
                        
                    }
                )


#
