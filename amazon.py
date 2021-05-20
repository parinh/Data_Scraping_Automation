from bs4 import BeautifulSoup
import csv

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
        product.append(_id)

        # Get Name
        name = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-base-plus.a-color-base.a-text-normal" )
        if (name):
            _name = name.text
        product.append(_name)
        
        # Price
        price = soup.select_one("span.a-price > span.a-offscreen")
        if (price):
            _price = price.text
        product.append(_price)

        # rating
        rating = soup.select_one("i > span.a-icon-alt")
        if (rating):
            _rating = rating.text
        product.append(_rating)
        
        #review
        review = soup.select_one("a.a-link-normal > span.a-size-base")
        if (review):
            _review = review.text
        product.append(_review)

        #best?
        bestseller = soup.select_one("div.a-row.a-badge-region > span.a-badge > span.a-badge-label > span.a-badge-label-inner.a-text-ellipsis > span.a-badge-text ")
        if(bestseller):
            _bestseller = bestseller.text
        product.append(_bestseller)
            
        imgs = soup.select_one("img.s-image")
        if (imgs):  
            _image = imgs['src']
        product.append(_image)

        #post url
        post_url = soup.select_one("span.rush-component > a.a-link-normal.s-no-outline")
        if(post_url):
            _url = "https://www.amazon.com/"+post_url['href']
        product.append(_url)

        return product
        
    def getData(self,html):
        soup = BeautifulSoup(html, "html.parser")
        
        for item in soup.find_all('div',  class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'):
            self.products.append(self.getItem(item))
        


    def toCsv(self,products):
        with open('amazon-search.csv', 'w', newline='') as csvfile:
            head_csv = ["num","id","name","price","rating","review","rank","img_src","url"]
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
                        "rating": products[i][3],
                        "review":products[i][4],
                        "rank":products[i][5],
                        "img_src":products[i][6],
                        "url":products[i][7]
                    }
                )
                

                
