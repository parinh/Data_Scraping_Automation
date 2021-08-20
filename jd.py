from os import name
from bs4 import BeautifulSoup
import csv
import json
from numpy import product, select
from numpy.lib.type_check import imag
from decouple import config


class JD:
    def __init__(self) :
        self.csv_count = 0
        self.products = []

    def getProducts(self,html):
        soup = BeautifulSoup(html,"html.parser")
        products = soup.select_one('pre')
        info = json.loads(products.text)
        for item in info['wareInfo'] :    
            self.products.append(self.getItem(item))
        return(len(self.products))
           
    
    def getItem(self,item):
        product = []
        _price = 'no price'
        _image = 'no image'
        _from = 'no data'
        _id = 'no id'
        _review = "no review"
        _type = 'general'
        _url = "no url"
        # ID
        try:
            _id = item['spuId']
        except:
            _id = 'no id'
            
        # Name
        try:
            _name = item['wname']
        except:
            _name = 'no name'

        # Price
        try:
            _price = float(item['jdPrice'])
        except:
            _price = 'no price'

        # Type
        try:
            _type = item['shopName']
        except:
            _type = 'general'
            
        # Review
        try:
            _review = int((item['reviews']).split(" ")[0])
        except:
            _review = "no review"

        # Img
        try:
            _image = item['imageurl']
        except:
            _image = 'no image'
            
        # From
        try:
            _from = item['localDelivery']
        except:
            _from = 'no data'

        # Url
        try:
            _url = "https://www.jd.co.th/product/"+ _id +".html"
        except:
            _url = "no url"

        
        product = {
            "name" : _name,
            "id" : _id,
            "price" : _price,
            "img_src":_image,
            "type" : _type,
            "review" : _review,
            "from" : _from,
            "url" : _url
        }
        return product

    def toCsv(self,products):
        with open(config("FILE"),'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","name","product_id","price","img_src","type","review","send_from","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(products)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "name" : products[i]['name'],
                        "product_id" : products[i]['id'],
                        "review" : products[i]['review'],
                        "price" : products[i]['price'],
                        "img_src":products[i]['img_src'],
                        "send_from" :products[i]['from'],
                        "type" : products[i]['type'],
                        "url" : products[i]['url']
                    }
                )
                

            

    
