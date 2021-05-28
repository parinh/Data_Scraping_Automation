from pythainlp import *
from pythainlp.tag.named_entity import ThaiNameTagger


class NLP:
    def __init__(self):
        self.positive_words = []
        self.negative_words = []
        self.swear_words = []
        self.check_words = []

        with open("word/negative-sentiment-words.txt",'r',encoding='utf-8') as f:
            for line in f:
                self.negative_words.append(line.rstrip())

        with open("word/positive-sentiment-words.txt", 'r',encoding='utf-8') as f:
            for line in f:
                self.positive_words.append(line.rstrip())
                
        with open("word/swear-words.txt", 'r',encoding='utf-8') as f:
            for line in f:
                self.swear_words.append(line.rstrip())

        

        
    def check(self,string):
        score = 0
        good = []
        bad = []
        ner = ThaiNameTagger()
        words = ner.get_ner(string)
        self.check_words.append(string)
        for word in words:
            if word in self.positive_words:
                if word not in good:
                    score = score + 1
                else:
                    score = score + 0.5
                good.append(word)

            if word in self.negative_words:
                if word not in bad:
                    score = score - 1
                else:
                    score = score - 0.5
                bad.append(word)

        self.check_words.append(good)
        self.check_words.append(bad)
        self.check_words.append(score)




