from pythainlp import *
from pythainlp.tag.named_entity import ThaiNameTagger
from pythainlp.corpus.common import thai_words
from pythainlp.util import dict_trie
from decouple import config

newWords = ["ไม่ดี","ไม่พอใจ","ชั่วคราว"]
custom_words_list = set(thai_words())
custom_words_list.update(newWords)
trie = dict_trie(dict_source=custom_words_list)
custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm',keep_whitespace=False)

class NLP:
    def __init__(self):
        self.positive_words = []
        self.negative_words = []
        self.swear_words = []
        self.check_words = []

        with open(config("NEGATIVE_SENTIMENT_WORDS"),'r',encoding='utf-8') as f:
            for line in f:
                self.negative_words.append(line.rstrip())

        with open(config("POSITIVE_SENTIMENT_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.positive_words.append(line.rstrip())
                
        with open(config("SWEAR_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.swear_words.append(line.rstrip())

        
    def check(self,string):
        print("1")
        words = custom_tokenizer.word_tokenize(string)
        score = 0
        good = []
        bad = []
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
        self.check_words.append(score)
        
        if(score>0):
            self.check_words.append('positive')
        elif(score==0):
            self.check_words.append('neutral')
        else: 
            self.check_words.append('negative')

        self.check_words.append(good)
        self.check_words.append(bad)
       

    def clearCheckWord(self):
        self.check_words.clear()
    

