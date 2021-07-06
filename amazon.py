from bs4 import BeautifulSoup
import csv
from decouple import config

class Amazon: 
    def __init__(self) :
        self.csv_count = 0
        self.products = []
    
    def getItem(self,soup):
        product = []
        _name = 'no name'
        _id = 'no id'
        _price = 'out of stock'
        _rating = 'no rating'
        _review = 'no review'
        _image = 'no image'
        _url = 'no url'
        _bestseller = 'not be a best'
   
        #item id
        item_code = soup['data-asin']
        if (item_code):  
            _id = item_code

        #  Name
        name = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-base-plus.a-color-base.a-text-normal" )
        if (name):
            _name = name.text
        
        # Price
        price = soup.select_one("span.a-price > span.a-offscreen")
        if (price):
            _price = float((price.text).split("$")[1])

        # rating
        rating = soup.select_one("i > span.a-icon-alt")
        if (rating):
            _rating = float((rating.text).split(" ")[0])
        
        #review
        review = soup.select_one("a.a-link-normal > span.a-size-base")
        if (review):
            _review = review.text
        

        #best?
        bestseller = soup.select_one("div.a-row.a-badge-region > span.a-badge > span.a-badge-label > span.a-badge-label-inner.a-text-ellipsis > span.a-badge-text ")
        if(bestseller):
            _bestseller = bestseller.text
            
        imgs = soup.select_one("img.s-image")
        if (imgs):  
            _image = imgs['src']
       
        #post url
        post_url = soup.select_one("span.rush-component > a.a-link-normal.s-no-outline")
        if(post_url):
            _url = "https://www.amazon.com/"+post_url['href']

        product = {
            "name": _name,
            "id": _id,
            "price": _price, 
            "rating": _rating, 
            "review": _review,
            "img_src": _image,
            "url": _url,
            "bestseller" : _bestseller
        }
        return product
        
    def getData(self,html):
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.select('div[data-component-type=s-search-result]'):
            self.products.append(self.getItem(item))
        


    def toCsv(self,products):
        with open(config("FILE"), 'w', newline='',encoding="utf-8") as csvfile:
            head_csv = ["num","product_id","name","price","rating","review","img_src","url","rank"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(products)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "name" : products[i]['name'],
                        "product_id" : products[i]['id'],
                        "price": products[i]['price'],
                        "rating" :products[i]['rating'],
                        "review":products[i]['review'],
                        "img_src" :products[i]['img_src'],
                        "url" : products[i]['url'],
                        "rank" : products[i]['bestseller']
                    }
                )
                

                
