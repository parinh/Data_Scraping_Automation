from os import name
from bs4 import BeautifulSoup
import csv

from numpy import product, select


import tocsv

class JD:
    def __init__(self) :
        self.csv_count = 0
        self.products = []

    def getProducts(self,html):
        
        soup = BeautifulSoup(html,"html.parser")
        for product in soup.find_all('li',class_="gl-item high") :
            self.products.append(self.getItem(product))

    # def getDataFromPostForJD(html):
    #     print ("get data JD")
    #     soup = BeautifulSoup(html, "html.parser")
    #     #big loop
    #     item_n = soup.select_one('pre')
    #     info = json.loads(item_n.text)
    #     for item in info['wareInfo'] :
    #         print (item['wname'])
    #         data = getItemDataForJD(item)
    #         products.append(data)

    def getItem(self,soup):
        product = []

        id = soup.select_one("div.gl-i-wrap.j-sku-item.imgscroll > section > div.p-price > strong")['id']
        product.append(id)

        return product




