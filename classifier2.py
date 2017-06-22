# -*- coding: utf-8 -*-

import random
from reader import read
from preprocess import preprocess
from preprocess import get_sub_dict
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords as sw
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class Classifier():

    def __init__(self):
        self.offset = 1000
        self.faq = []
        self.sub_dict = dict()
        self.answers = dict()
        self.sub_dict = get_sub_dict(self.sub_dict, 'siglas')
        self.sub_dict = get_sub_dict(self.sub_dict, 'academico')
        self.sub_dict = get_sub_dict(self.sub_dict, 'abreviacoes')
        self.sub_dict = get_sub_dict(self.sub_dict, 'conjuntos')
        self.sub_dict = get_sub_dict(self.sub_dict, 'sinonimos')
        self.read_faq()
        random.shuffle(self.faq)
        """        
        test_set = []
        train_set = []
        my_set = set([x[1] for x in self.faq])
        for cl in my_set:
            sen = [x[0] for x in self.faq if x[1] == cl]
            test_set += [(sen.pop(),cl)]
            test_set += [(sen.pop(),cl)]
            train_set += [(s,cl) for s in sen]
        faq_treino = [x[0] for x in train_set]
        class_treino = [x[1] for x in train_set]
        faq_teste = [x[0] for x in test_set]
        class_teste = [x[1] for x in test_set]
        """
        trial = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', RandomForestClassifier(n_estimators=140, max_features=3)),
        ])
        train_faq = [x[0] for x in self.faq]
        train_class = [x[1] for x in self.faq]
        self.classifier = trial.fit(train_faq,train_class)
        """
        print 'Accuracy'
        print self.classifier.score(faq_teste,class_teste)
        print 'F1 Score'
        ans = self.classifier.predict(faq_teste)
        print (classification_report(class_teste,ans))
        """

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
        # sobre
        self.get_data('1AGkOlKeuGK8BtB92PTOlFYOiIdXvxQ9RRqJcf1_5vHo')
        # formacao complementar
        self.get_data('1IA2rFHmD5VESpzzWSG76wwqFvbU8f0IjczPgJumEMjQ')
        # matricula
        self.get_data('1T1FfsVpLdBntyAfW_Rv4CNgoD8imDOt52GTg5nsKnSM')

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
        ans = self.classifier.predict([sentence])
        return self.answers[ans[0]], 0

    def save(self):
        fc = open('classifier2.pickle', 'wb')
        pickle.dump(self, fc)
        fc.close() 
