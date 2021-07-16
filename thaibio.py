import csv
from bs4 import BeautifulSoup
from decouple import config
class ThaiBio :
    def __init__(self):
        self.datas = []
        self.csv_count = 0+900

    def getData(self,html):
        print("get data form shopee")
        soup = BeautifulSoup(html, "html.parser")
        data = {
            "group" : "",
            "thai_name" : ""
        }
        for item in soup.select('ol[id=general_information] > li.metaContent-item'):
            if ("กลุ่มทรัพยากรชีวภาพ" in item.select_one("div.title").text):
                _group = item.select_one("div.value").text
                data["group"] = _group
            if ("ชื่อพันธุ์ไทย" in item.select_one("div.title").text or "ชื่อไทย" in item.select_one("div.title").text or "ชื่อทั่วไป (Name)" in item.select_one("div.title")):
                _thai_name = item.select_one("div.value").text
                data["thai_name"] = _thai_name
            else:  
                pass
        print(data)
        self.datas.append(data)

    def toCsv(self, datas):
        with open(config("THAIBIO_FILE"), "a", encoding="utf-8", newline="") as csvfile:
            head_csv = ["num","group","thai_name"]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(datas)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "group": datas[i]["group"],
                        "thai_name": datas[i]["thai_name"]
                    }
                )

        
