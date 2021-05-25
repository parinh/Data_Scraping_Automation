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

    def getItem(self,soup):
        product = []

        id = soup.select_one("div.gl-i-wrap.j-sku-item.imgscroll > section > div.p-price > strong")['id']
        product.append(id)

        return product




