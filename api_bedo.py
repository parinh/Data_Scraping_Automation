from decouple import config
import csv

class ApiBedo:
    def __init__(self):
        self.datas = []
        self.csv_count = 0

    def getItem(self, result):
        data = {}
        _id = "no id"
        _name = "no name"
        _url = "no url"
        index_id = result.get("id")
        if(index_id):
            _id = index_id
        index_name = result.get("name")
        if(index_name):
            _name=index_name
        index_url = result.get("url")
        if(index_url):
            _url = index_url.replace("http://localhost", "http://api.bedo.or.th")
        
        data = {
            "id": _id,
            "name": _name,
            "url": _url
        }
        return data

    def getData(self, results):
        for result in results:
            self.datas.append(self.getItem(result))

    def toCsv(self,datas,filename):
        with open(config(filename), "w", encoding="utf-8", newline="") as csvfile:
            head_csv = ["num","id","name","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames=head_csv)
            thewriter.writeheader()
            for i in range(len(datas)):
                print(i)
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "id": datas[i]["id"],
                        "name": datas[i]["name"],
                        "url": datas[i]["url"]
                    }
                )
