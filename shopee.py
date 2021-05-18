from bs4 import BeautifulSoup
import csv

class Shopee:
    #get item
    def getItemDataForShopee(self,soup):
        a=[]
        
        #id
        # s = soup.select_one("a")
        # item_id = s['href'].split(".")[len(s['href'].split("."))-2]
        # print(item_id)
        # item_id = s['href'].split(".")[len(s['href'].split("."))-1]
        # print(item_id)
        # print("\n")
       
        # a.append(item_id)
        
        # Name
        for item_n in soup.find_all('div', class_='yQmmFK _1POlWt _36CEnF'):
            a.append(item_n.get_text())
           
        # Price
        for item_c in soup.find_all('div', class_='WTFwws _1lK1eK _5W0f35'):
            a.append(item_c.get_text()) 
            
        # find total number of items sold/month *********
        for items_s in soup.find_all('div',class_ = 'go5yPW'):
            a.append(items_s.get_text())
           
        #from
        for items_f in soup.find_all('div',class_ = '_2CWevj'):
            a.append(items_f.get_text())
           
        # img path
        for imgs in soup.find_all('div', class_ = '_25_r8I _2SHkSu'):
            a.append(imgs.select("img")[0]['src'])
        
        return a
    
    #add data in array
    def getDataFromPostForShopee(self,html):
        soup = BeautifulSoup(html, "html.parser")
        b=[]
        # print(soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'))
        for item in soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'):
            # print(item.get_text())
            if(item.select_one('div.shopee-image-placeholder')):
                continue  
            else:  
                b.append(self.getItemDataForShopee(item))

        return b
    
    def toCsv(arr):
        csv_count = 0
        with open('myfile.csv', 'w', newline='') as csvfile:
            head_csv = ["num","id","name","price","rating","review","img_src"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(arr)):
                thewriter.writerow({"num": csv_count,"id": arr[i][0],"name": arr[i][1],"price": arr[i][2],"rating": arr[i][3],"review":arr[i][4],"img_src":arr[i][5]})
                csv_count += 1
# 



