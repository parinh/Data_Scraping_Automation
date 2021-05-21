from bs4 import BeautifulSoup
from lxml import html
import json
import requests
from requests.api import post
from requests.exceptions import ConnectionError, ReadTimeout
import csv


class Pantip:

    def __init__(self) :
        self.csv_count = 0
        self.posts = []

    def getPosts(self,html):
        soup = BeautifulSoup(html, "html.parser")
        for post in soup.find_all('div',class_='rowsearch card px-0'):
            post_url = post.select_one("div.rowsearch.card.px-0 > div.title.col-md-12 > a.datasearch-in")
            # print(post_url['href'])
            self.posts.append(self.getItem(post_url['href']))

    def getItem(self,link):
        post = []
        start_page = requests.get(link)
        start_page.encoding = 'utf-8'
        tree = html.fromstring(start_page.text)

        id = link.split("/")[len(link.split("/"))-1]
        post.append(id)

        title = tree.xpath('//h2[@class="display-post-title"]/text()')[0]
        post.append(title)

        description = tree.xpath('//div[@class="display-post-story"]')[0].text_content()
        post.append(description)

        author = tree.xpath('//a[@class="display-post-name owner"]/text()')[0]
        post.append(author)

        # author_id = tree.xpath('//a[@class="display-post-name owner"]/@id')[0]
        # post.append(author_id)

        likeCount = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
        post.append(likeCount)

        emoCount = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
        post.append(emoCount)
        # allEmos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
        # post.append(allEmos)
        # tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item"]/text()')
        # post.append(tags)
        dateTime = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]
        post.append(dateTime)

        post.append(link)

        return post

    def toCsv(self,posts):
        with open('pantip-search.csv', 'w', encoding='utf-8',newline='') as csvfile:
            head_csv = ["num","id","title","description","author","like","emo","date-time","url"]
            thewriter = csv.DictWriter(csvfile, fieldnames = head_csv)
            thewriter.writeheader()

            for i in range(len(posts)):
                self.csv_count += 1
                thewriter.writerow(
                    {
                        "num": self.csv_count,
                        "id": posts[i][0],
                        "title": posts[i][1],
                        "description": posts[i][2],
                        "author": posts[i][3],
                        "like":posts[i][4],
                        "emo":posts[i][5],
                        "date-time":posts[i][6],
                        "url":posts[i][7]
                        
                    }
                )


        
        
        
#     def get_topic_from_link(tid):
# 		global udg_header
# 		index = 0
# 		while(index < 4):
# 			start_page = requests.get("http://pantip.com/topic/%s"%(tid), 
# 				headers=udg_header_comment)
# 			if (start_page.reason == 'OK'):
# 				break
# 			else:
# 				index = index + 1
# 			if index == 4:
# 				rData = ReturnData(False, "Cannot open page %s: "%(tid) + start_page.reason)
# 				return rData

# 		start_page.encoding = udg_thaiEncode
# 		tree = html.fromstring(start_page.text)

# 		tmp = tree.xpath('//div[starts-with(@class,"callback-status")]')
# 		if tmp and tmp[0].text_content():
# 			if not tree.xpath('//h2[@class="display-post-title"]/text()'):
# 				rData = ReturnData(False, tree.xpath('//div[starts-with(@class,"callback-status")]')[0].text_content().strip())
# 				return rData

# 		name = tree.xpath('//h2[@class="display-post-title"]/text()')[0]
# 		author = tree.xpath('//a[@class="display-post-name owner"]/text()')[0]
# 		author_id = tree.xpath('//a[@class="display-post-name owner"]/@id')[0]
# 		story = tree.xpath('//div[@class="display-post-story"]')[0].text_content()
# 		likeCount = tree.xpath('//span[starts-with(@class,"like-score")]/text()')[0]
# 		emoCount = tree.xpath('//span[starts-with(@class,"emotion-score")]/text()')[0]
# 		allEmos = tree.xpath('//span[@class="emotion-choice-score"]/text()')
# 		tags = tree.xpath('//div[@class="display-post-tag-wrapper"]/a[@class="tag-item"]/text()')
# 		dateTime = tree.xpath('//abbr[@class="timeago"]/@data-utime')[0]

# 		emotions = Emotion(allEmos[0], allEmos[1], allEmos[2], allEmos[3], allEmos[4], allEmos[5])
# 		topic = Topic(tid, name, author, author_id, story, likeCount, emoCount, emotions, tags, dateTime)
# 		rData = ReturnData(True, topic)
# 		return rData
