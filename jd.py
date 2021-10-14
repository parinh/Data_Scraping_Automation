from bs4 import BeautifulSoup
import csv
import json
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
        _price = 0
        _image = 'no image'
        _from = 'no data'
        _id = 0
        _review = "no review"
        _type = 'general'
        _url = "no url"
        # ID
        try:
            __id = item['spuId']
            if(__id):
                _id = __id
        except:
            pass
            
        # Name
        try:
            __name = item['wname']
            if(__name):
                _name = __name
        except:
            pass

        # Price
        try:
            __price = float(item['jdPrice'])
            if(__price):
                _price = __price
        except:
            pass

        # Type
        try:
            __type = item['shopName']
            if(__type):
                _type = __type
        except:
            pass
            
        # Review
        try:
            __review = int((item['reviews']).split(" ")[0])
            if(__review):
                _review = __review
        except:
            pass

        # Img
        try:
            __image = item['imageurl']
            if(__image):
                _image = __image
        except:
            pass
            
        # From
        try:
            __from = item['localDelivery']
            if(__from):
                _from = __from
        except:
            pass

        # Url
        try:
            __url = "https://www.jd.co.th/product/"+ _id +".html"
            if(__url):
                _url = __url
        except:
            pass

        
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
                

            

    
