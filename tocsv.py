import csv

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
        with open(self.file_name, 'w', newline='') as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)
            thewriter.writeheader()

    def addData (self,products):
        with open(self.file_name, mode='a', newline='') as csvfile:
            thewriter = csv.DictWriter(csvfile, fieldnames = self.header_field)

            for i in range(len(products)):
                
                thewriter.writerow(
                    {
                        "num": self.num,
                        "name" : products[i]['name'],
                        "price" : products[i]['price'],
                        "sold": products[i]['sold'],
                        "from" :products[i]['from'],
                        "img_src":products[i]['img_src'],
                        "url" :products[i]['url'],
                        "type" : products[i]['type']
                    })
                self.num +=1
        # self.thewriter.writerows({"num": self.count,"name": products[i]['name'],"price": products[i]['price'],"type": products[i]['type'],"sold": products[i]['sold'],"from": products[i]['from'],"img_src": products[i]['image'],"url" : products[i]['url']})
