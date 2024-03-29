from bs4 import BeautifulSoup
import csv
from decouple import config


class Amazon: 
    def __init__(self) :
        self.csv_count = 0
        self.products = []
        self.details = []
    
    def getItem(self,soup):
        product = []
        _name = 'no name'
        _id = 'no id'
        _price = 'out of stock'
        _rating = 0
        _review = 0
        _image = 'no image'
        _url = 'no url'
        _bestseller = 'not be a best'
   
        try:
            #item id
            try:
                item_code = soup['data-asin']
                if (item_code):  
                    _id = item_code
            except Exception as e:
                pass
            

            #  Name
            try:
                name = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-base-plus.a-color-base.a-text-normal" )
                if (name):
                    _name = name.text
                else:
                    name = soup.select_one("a.a-link-normal.a-text-normal > span.a-size-medium.a-color-base.a-text-normal")
                    if (name):
                        _name = name.text
            except Exception as e:
                pass
            
            # Price
            try:
                price = soup.select_one("span.a-price > span.a-offscreen")
                if (price):
                    _price = float((price.text).split("$")[1])
            except Exception as e:
                pass

            # rating
            try:
                rating = soup.select_one("i > span.a-icon-alt")
                if (rating):
                    _rating = float((rating.text).split(" ")[0])
            except Exception as e:
                pass
            #review
            # a.a-link-normal > span.a-size-base
            try:
                review = soup.select_one("div.a-section.a-spacing-none.a-spacing-top-micro > div.a-row.a-size-small > span > a.a-link-normal > span.a-size-base")
                if (review):
                    _review = float("".join(review.text.split(",")))
                    # _review = review.text
            except Exception as e:
                pass
            # print("\n")
            

            #best?
            try:            
                bestseller = soup.select_one("div.a-row.a-badge-region > span.a-badge > span.a-badge-label > span.a-badge-label-inner.a-text-ellipsis > span.a-badge-text ")
                if(bestseller):
                    _bestseller = bestseller.text
            except Exception as e:
                pass

            try:
                imgs = soup.select_one("img.s-image")
                if (imgs):  
                    _image = imgs['src']
            except Exception as e :
                pass

            try:
            #post url
                post_url = soup.select_one("span.rush-component > a.a-link-normal.s-no-outline")
                if(post_url):
                    _url = "https://www.amazon.com/"+post_url['href']
            except Exception as e:
                pass
        except:
            print("something wrong")
            
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
            # print(item,"\n")
            self.products.append(self.getItem(item))
        return(len(self.products))
        
    def getDetail(self,product_id,html):
        _brand  = "no brand"
        _description = "no description"
        
        try:
            soup = BeautifulSoup(html,"html.parser")
            brand = ""
            for item in soup.select("tr.a-spacing-small"):
                if item.select_one("td.a-span3 > span").text == 'Brand':
                    brand = item.select_one("td.a-span9 > span.a-size-base").text
                    break
            if(brand):
                _brand=brand
            else:
                try:
                    brand = soup.select_one("#bylineInfo").text
                    if "Brand:" in brand:
                        brand = brand.split("Brand: ")[1]
                        _brand = brand
                    if "Visit" in brand:
                        brand = brand.split("Visit the ")[1].split("Store")[0]
                        _brand = brand

                    else:
                        brand = soup.select_one("div.a-section.feature.detail-bullets-wrapper.bucket > div[id=detailBullets_feature_div] ")
                        for row in brand.select("li"):
                            if("Publisher" in row.text):
                                row = row.select("span")[2].text.split(";")[0]
                                _brand = row
                                # print(_brand)
                                break
                            
            
                except:
                    pass

        except Exception as e:
            pass

        try:
            description = ""
            for item in soup.select("ul.a-unordered-list.a-vertical.a-spacing-mini > li "):
                description += item.text
            
            if(description):
                _description=description
            else:
                description = soup.select_one("div[id=editorialReviews_feature_div]")
                if(description):
                    _description=description.text
        except: pass

        detail = {
            "product_id": product_id,    
            "brand": _brand,
            "description": _description 
        }

        self.details.append(detail)


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
                

    def detailToCsv(self,details):
        with open(config("FILE"), "w", encoding="utf-8", newline="") as csvfile:
            head_csv = [
                "product_id",
                "brand",
                "description",
            ]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(details)):
                thewriter.writerow(
                    {
                        "product_id": details[i]["product_id"],
                        "brand": details[i]["brand"],
                        "description": details[i]["description"],
                    }
                )

