import csv
from datetime import datetime


class Tocsv:
    file_name = "my_csv.csv"
    num = 1

    def __init__(self,  file_name, header_field=[]):
        self.header_field = header_field
        self.file_name = file_name
       

    def setHeader (self,header_field):
        self.header_field = header_field
        self.createFile()


    def createFile(self) :
        with open(self.file_name, 'w', newline='',encoding="utf-8") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)
            thewriter.writeheader()




    def addDataForShopee (self,products):
        with open(self.file_name, mode='a', newline='',encoding="utf-8") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)

            for i in range(len(products)):
                
                thewriter.writerow(
                    {
                        "num": self.num,
                        "name" : products[i]['name'],
                        "price" : products[i]['price'],
                        "sold": products[i]['sold'],
                        "star" : products[i]['star'],
                        "from" :products[i]['from'],
                        "img_src":products[i]['img_src'],
                        "url" :products[i]['url'],
                        "type" : products[i]['type'],
                        "id" :products[i]['id']
                    })
                self.num +=1
        # self.thewriter.writerows({"num": self.count,"name": products[i]['name'],"price": products[i]['price'],"type": products[i]['type'],"sold": products[i]['sold'],"from": products[i]['from'],"img_src": products[i]['image'],"url" : products[i]['url']})
    

    def addDataForAmazon (self,products):
        with open(self.file_name, mode='a', newline='',encoding="utf-8") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)

            for i in range(len(products)):
                
                thewriter.writerow(
                    {
                        "num": self.num,
                        "name" : products[i]['name'],
                        "id" : products[i]['id'],
                        "price": products[i]['price'],
                        "rating" :products[i]['rating'],
                        "review":products[i]['review'],
                        "img_src" :products[i]['img_src'],
                        "url" : products[i]['url'],
                        "rank" : products[i]['bestseller']
                    })
                self.num +=1


    
    def addDataForPantip (self,products):
        products.sort(key=lambda x: datetime.strptime(x['dateTime'], "%m/%d/%Y %H:%M:%S") ,reverse = True)
        with open(self.file_name, mode='a', newline='',encoding="utf-8") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)

            for i in range(len(products)):
                
                thewriter.writerow(
                    {
                        "num": self.num,
                        "title" : products[i]['title'],
                        "author" : products[i]['author'],
                        "author_id": products[i]['author_id'],
                        "story" :products[i]['story'],
                        "likeCount":products[i]['likeCount'],
                        "emocount" :products[i]['emocount'],
                        "allemos" : products[i]['allemos'],
                        "tags" : products[i]['tags'],
                        "dateTime" : products[i]['dateTime'],
                        "post_link" : products[i]['post_link'],
                        "img_src" : products[i]['img_src'],
                        "post_id" : products[i]['post_id'],
                        "meaning" : products[i]['meaning'],
                        "goodWords" : products[i]['goodWords'],
                        "badWords" : products[i]['badWords']
                    })
                self.num +=1


    def addDataForJD (self,products):
        # products.sort(key=lambda x: datetime.strptime(x['dateTime'], "%m/%d/%Y %H:%M:%S") ,reverse = True)
        with open(self.file_name, mode='a', newline='',encoding="utf-8") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)

            for i in range(len(products)):
                
                thewriter.writerow(
                    {
                        "num": self.num,
                        "name" : products[i]['name'],
                        "id" : products[i]['id'],
                        "review" : products[i]['review'],
                        "price" : products[i]['price'],
                        "img_src":products[i]['img_src'],
                        "from" :products[i]['from'],
                        "type" : products[i]['type'],
                        "url" : products[i]['url']
                        
                    })
                self.num +=1

    
    def addDataForFacebook (self,products):
        # products.sort(key=lambda x: datetime.strptime(x['dateTime'], "%m/%d/%Y %H:%M:%S") ,reverse = True)
        with open(self.file_name, mode='a', newline='',encoding="utf-8") as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)

            for i in range(len(products)):
                
                thewriter.writerow(
                    {
                        "num": self.num,
                        "user_name" : products[i]['user_name'],
                        "comment" : products[i]['comment'],
                        "date" : products[i]['date'],
                        "image_h" : products[i]['image_h'],
                        "image_l":products[i]['image_l'],
                        "reaction" :products[i]['reaction'],
                        "post_url" : products[i]['post_url'],
                        "post_id" : products[i]['post_id'],
                        "post_text" : products[i]['post_text'],
                        "meaning" : products[i]['meaning'],
                        "goodWords" : products[i]['goodWords'],
                        "badWords" : products[i]['badWords']

                        
                    })
                self.num +=1