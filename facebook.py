from facebook_scraper import *


class Facebook:
    def __init__(self):
        self.csv_count =0
        self.posts =[]

    def getPosts(self,page_id,page_count):
        for post in get_posts(account=page_id,pages=page_count):
            self.posts.append(post)
            # print(post)
        
    def toCsv(self,posts):
        with open('csv/facebook-posts.csv','w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","text","like","comment","shared","date_time","img_src","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(posts)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "id": posts[i]['post_id'],
                        "text": posts[i]['text'],
                        "like": posts[i]['reactions']['like'],
                        "comment": posts[i]['comments'],
                        "shared": posts[i]['shares'],
                        "date_time": posts[i]['time'],
                        "img_src":posts[i]['image'],
                        "url":posts[i]['w3_fb_url']
                    }
                )