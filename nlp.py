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
        is_food = 0
        is_health = 0
        is_beauty = 0
        is_spa = 0
        is_travel = 0
        nlp = []

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

            if word in self.beauty_words:
                beauty.append(word)
                is_beauty = 1
            if word in self.spa_words:
                spa.append(word)
                is_spa = 1
            if word in self.travel_words:
                travel.append(word)
                is_travel = 1
            if word in self.health_words:
                health.append(word)
                is_health = 1
            if word in self.beauty_words:
                beauty.append(word)
                is_beauty = 1
        
        if(score>0):
            # self.check_words.append('positive')
            meaning = 'positive'
        elif(score==0):
            # self.check_words.append('neutral')
            meaning = 'neutral'
        else: 
            # self.check_words.append('negative')
            meaning = 'negative'

        self.check_words = {
            'score':score,
            'good_words': good,
            'bad_words': bad,
            'meaning': meaning,
            'food_words': food,
            'health_words': health,
            'beauty_words': beauty,
            'spa_words': spa,
            'travel_word': travel,
            'is_food': is_food,
            'is_beauty': is_beauty,
            'is_health': is_health,
            'is_spa': is_spa,
            'is_travel': is_travel
        }
        

    def clearCheckWord(self):
        self.check_words.clear()
    

