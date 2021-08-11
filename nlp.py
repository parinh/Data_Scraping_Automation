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
        self.food_words = []
        self.spa_words = []
        self.beauty_words = []
        self.travel_words = []
        self.health_words = []

        with open(config("NEGATIVE_SENTIMENT_WORDS"),'r',encoding='utf-8') as f:
            for line in f:
                self.negative_words.append(line.rstrip())

        with open(config("POSITIVE_SENTIMENT_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.positive_words.append(line.rstrip())
                
        with open(config("SWEAR_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.swear_words.append(line.rstrip())
        
        with open(config("FOOD_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.food_words.append(line.rstrip())
        
        with open(config("SPA_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.spa_words.append(line.rstrip())

        with open(config("HEALTH_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.health_words.append(line.rstrip())

        with open(config("TRAVEL_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.travel_words.append(line.rstrip())

        with open(config("BEAUTY_WORDS"), 'r',encoding='utf-8') as f:
            for line in f:
                self.beauty_words.append(line.rstrip())
        
    def check(self,string):
        words = custom_tokenizer.word_tokenize(string)
        score = 0
        meaning = ''
        good = []
        bad = []
        beauty = []
        food = []
        spa = []
        travel = []
        health = []

        _good = []
        _bad = []
        _beauty = []
        _food = []
        _spa = []
        _travel = []
        _health = []
        food_words_count = 0
        health_words_count = 0
        beauty_words_count = 0
        spa_words_count = 0
        travel_words_count = 0
        nlp = []

        for word in words:

            if word in self.positive_words:
                if word not in good:
                    score = score + 1
                    _good.append(word)
                else:
                    score = score + 0.5

            if word in self.negative_words:
                if word not in bad:
                    score = score - 1
                    _bad.append(word)
                else:
                    score = score - 0.5

            if word in self.food_words:
                if (word not in food):
                   _food.append(word)  
                food_words_count += 1

            if word in self.spa_words:
                if (word not in spa):
                    _spa.append(word)
                spa_words_count += 1

            if word in self.travel_words:
                if (word not in travel):
                    _travel.append(word)
                travel_words_count += 1

            if word in self.health_words:
                if (word not in health):
                    _health.append(word)
                health_words_count += 1

            if word in self.beauty_words:
                if (word not in beauty):
                    _beauty.append(word)
                beauty_words_count += 1
        
        if(score>0):
            meaning = 'positive'
        elif(score==0):
            meaning = 'neutral'
        else: 
            meaning = 'negative'
        
        good = ",".join(_good)
        bad = ",".join(_bad)
        food = ",".join(_food)
        health = ",".join(_health)
        beauty = ",".join(_beauty)
        spa = ",".join(_spa)
        travel = ",".join(_travel)

        self.check_words = {
            'score':score,
            'good_words': good,
            'bad_words': bad,
            'meaning': meaning,
            'food_words': food,
            'health_words': health,
            'beauty_words': beauty,
            'spa_words': spa,
            'travel_words': travel,
            'food_words_count': food_words_count,
            'beauty_words_count': beauty_words_count,
            'health_words_count': health_words_count,
            'spa_words_count': spa_words_count,
            'travel_words_count': travel_words_count,
        }
        

    def clearCheckWord(self):
        self.check_words.clear()
    

