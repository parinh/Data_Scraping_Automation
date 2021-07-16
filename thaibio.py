
class ThaiBio :
    def __init__(self):
        self.datas = []

    def getData(self,soup):
        i = soup.select_one("div.bs-callout.bs-callout-info")
        # for item in soup.select("div[bs-callout bs-callout-info]"):
        print(1)
        print(i)
