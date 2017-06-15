# -*- coding: utf-8 -*-

import random
from nltk import FreqDist
from nltk import NaiveBayesClassifier as nb
from nltk import DecisionTreeClassifier as dt
from nltk.classify import apply_features
from nltk.metrics.distance import edit_distance
from reader import read
from preprocess import preprocess
from preprocess import get_sub_dict
import pickle

class Classifier():

    def __init__(self):
        self.word_frequency = FreqDist()
        self.offset = 1000
        self.faq = []
        self.sub_dict = dict()
        self.answers = dict()
        self.sub_dict = get_sub_dict(self.sub_dict, 'siglas')
        self.sub_dict = get_sub_dict(self.sub_dict, 'academico')
        self.sub_dict = get_sub_dict(self.sub_dict, 'abreviacoes')
        self.sub_dict = get_sub_dict(self.sub_dict, 'conjuntos')
        self.read_faq()
        random.shuffle(self.faq)
        self.get_word_frequency()
        train_set = apply_features(self.extract_feature, self.faq)
        self.classifier = nb.train(train_set)
 
    def get_word_frequency(self):
        for t in self.faq: 
            question = t[0]
            words = set(question.split(' '))
            freq = 1
            if len(words) <= 2:
                freq = 10
            for word in words:
                self.word_frequency[word.lower()] += freq

    def extract_feature(self, sentence):
        bow = set(sentence.lower().split(' '))
        features = {}
        #for word in self.word_frequency.keys():
        #    features[word] = (word in bow)
        freq = 1
        if len(bow) <= 2:
            freq = 10
        for freq_word in self.word_frequency.keys():
            for word in bow:
                if edit_distance(freq_word,word) <= 2:
                    if freq_word in features:
                        features[freq_word] += freq
                        break
                    else:
                        features[freq_word] = freq
                        break
                    #break
        return features

    def read_faq(self):
        # colegiado
        self.get_data('1fqDkqnZ1Zws5yrAa7cZryJKZO2hQDrqU2kW64SA8zAo')
        # apresentacao
        self.get_data('1IxnEQxrArzEJvoCzdISERzkCEkzM6heVO58FN3F7c9Y')
        # biblioteca
        self.get_data('1U8t-blzZHM9m1K9H6O1eLYEv_EhuwVUGmrkzcU7STDQ')
        # informacoes_gerais
        self.get_data('1VXLnbmBo-OBtbFu9JfBSC0v8ufUBTT3sIwpXj5mz8Ec')
        # creditos
        self.get_data('1FwuOvzxT9pcvuYHIYoYQbByTwNwZWI0NW_WV8_YvPP8')
        # sobre_cursos
        self.get_data('1z_U7mDvru1dOkhjo62SInosYMzSpXPXBCUVobB7jgFk')

    def get_data(self, spreadsheetId):
        q = read(spreadsheetId,'pergunta')
        a = read(spreadsheetId,'resposta')
        for row in a:
            self.answers[int(row[0])+self.offset] = row[1]    
        for row in q:
            t = (preprocess(row[0],self.sub_dict),int(row[1])+self.offset)
            self.faq += [t]
        self.offset += 1000

    def get_answer(self, sentence):
        sentence = preprocess(sentence,self.sub_dict)
        p = self.classifier.prob_classify(self.extract_feature(sentence))
        #if p.prob(p.max()) <= 0.7:
        #    return 'Me desculpe, não consegui entender :(', p.prob(p.max())
        #ans = self.classifier.classify(self.extract_feature(sentence))
        ans = p.max()
        return self.answers[ans], p.prob(p.max())

    def save_classifier(self):
        fc = open('classifier.pickle', 'wb')
        pickle.dump(self, fc)
        fc.close() 
