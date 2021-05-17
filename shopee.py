from bs4 import BeautifulSoup



class Shopee:
    #get item
    def getItemDataForShopee(self,soup):
        a=[] 
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
            # a.append(5)
        
        return a
    
    #add data in array
    def getDataFromPostForShopee(self,html):
        soup = BeautifulSoup(html, "html.parser")
        b=[]
        for item in soup.find_all('div',  class_='col-xs-2-4 shopee-search-item-result__item'):
            print(item.get_text())
            b.append(self.getItemDataForShopee(item))

        return b




