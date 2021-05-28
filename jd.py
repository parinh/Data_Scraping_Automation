from os import name
from bs4 import BeautifulSoup
import csv
import json

from numpy import product, select
from numpy.lib.type_check import imag

import tocsv

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
           
    
    def getItem(self,item):
        product = []
        _name = 'no name'
        _price = 'no price'
        _image = 'no image'
        _from = 'no data'
        _id = 'no id'
        _review = "no review"
        _type = 'general'

        try:
            _id = item['spuId']
            product.append(_id)
        except:
            product.append(_id)

        try:
            _name = item['wname']
            product.append(_name)
        
        except:
            product.append(_name)

        try:
            _price = item['jdPrice']
            product.append(_price)
        except:
            product.append(_price)

        try:
            _type = item['shopName']
            product.append(_type)
        except:
            product.append(_type)

        try:
            _review = int((item['reviews']).split(" ")[0])
            product.append(_review)
        except:
            product.append(_review)

        try:
            _image = item['imageurl']
            product.append(_image)
        except:
            product.append(_image)
        
        try:
            _from = item['localDelivery']
            product.append(_from)
        except:
            product.append(_from)

        url = "https://www.jd.co.th/product/"+str(item['spuId'])+".html"
        product.append(url)




        return product

    def toCsv(self,products):
        with open('csv/jd-search.csv','w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","name","price","type","review","from","img_src","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(products)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "id": products[i][0],
                        "name": products[i][1],
                        "price": products[i][2],
                        "type": products[i][3],
                        "review":products[i][4],
                        "from":products[i][5],
                        "img_src":products[i][6],
                        "url":products[i][7]
                    }
                )
                

            

    
