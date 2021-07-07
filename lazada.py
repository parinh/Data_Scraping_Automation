from os import name
from bs4 import BeautifulSoup
import csv
import tocsv

class Lazada:
    def __init__(self) :
        self.csv_count = 0
        self.products = []

    def getProducts(self,html):
        soup = BeautifulSoup(html,"html.parser")
        for product in soup.find_all('div',class_='c2prKC'):
            self.products.append(self.getItem(product))

    def getItem(self,soup):
        product=[]
        link = soup.select_one('div.c3e8SH > div.c5TXIP > div.c2iYAv > div.cRjKsc > a')['href']
        product.append(link)

        return product


