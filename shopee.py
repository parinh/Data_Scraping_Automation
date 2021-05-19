from os import name
from bs4 import BeautifulSoup
import csv

from numpy import product

class Shopee:
    #get item
    def getItem(self,soup):
        product=[]
        _name = 'no name'
        _price = 'no price'
        _sold = 'no sold'
        _from = 'no from'
        _image = 'no image'
        _url = 'no url'
        _type = 'general'

        # Name 1
        name = soup.select_one("div._1nHzH4 > div.PFM7lj > div.yQmmFK._1POlWt._36CEnF" )
        if (name):
            _name = name.text
        product.append(_name)
       
        # Price 2
        price = soup.select_one("div.WTFwws._1lK1eK._5W0f35")
        if (price):
            _price = price.text
        product.append(_price)

        #type 3
        __type = soup.select_one("div.Oi0pcf.KRP-a_ > span._2_d9RP")
        if(__type):
            _type = __type.text
            

        __type = soup.select_one("div._1qt0vU > div.Oi0pcf._3Bekkv")
        # print(__type)
        if(__type):
            # product
            _type = "shopee mall"
        # else:
        #     print("general")
        product.append(_type)

        # sold/month 4
        sold = soup.select_one("div.go5yPW")
        if (sold.text):
            _sold = sold.text
        product.append(_sold) 
           
        #from 5
        __from = soup.select_one("div._2CWevj")
        if (__from):
            _from = __from.text
        product.append(_from)

        # find img path 6
        imgs = soup.select_one("div._25_r8I._2SHkSu > img")
        try:
            _image = imgs['src']
            product.append(_image)
         
        except:
            product.append(_image)
        
       #url 7
        url = soup.select_one("a")
        _url = "https://shopee.co.th/"+url['href']
        product.append(_url)
            
        return product


    #add data in array
    def getData(self,html):
        soup = BeautifulSoup(html, "html.parser")
        products=[]
        for item in soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'):
            if(item.select_one('div.shopee-image-placeholder')):
                continue  
            else:  
                products.append(self.getItem(item))

        return products
    
    def toCsv(self,products):
        csv_count = 0
        with open('shopee-search.csv', 'a', encoding="utf-8",newline='') as csvfile:
            head_csv = ["num","name","price","type","sold","from","img_src","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(products)):
                csv_count += 1
                thewriter.writerow({"num": csv_count,"name": products[i][0],"price": products[i][1],"type": products[i][2],"sold":products[i][3],"from":products[i][4],"img_src":products[i][5],"url":products[i][6]})
                
# 



