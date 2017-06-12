# -*- coding: utf-8 -*-

import random
from nltk import FreqDist
from nltk import NaiveBayesClassifier as nb
from nltk.classify import apply_features
from reader import read
from preprocess import preprocess
from preprocess import get_sub_dict

classifier = None
word_frequency = FreqDist()
offset = 1000
answers = dict()
faq = []

def create_classifier():
    sub_dict = dict()
    sub_dict = get_sub_dict(sub_dict,'siglas')
    sub_dict = get_sub_dict(sub_dict,'academico')
    sub_dict = get_sub_dict(sub_dict,'abreviacoes')
    sub_dict = get_sub_dict(sub_dict,'conjuntos')
    read_faq(sub_dict)
    global faq
    global classifier
    random.shuffle(faq)
    get_word_frequency()
    train_set = apply_features(extract_feature, faq)
    classifier = nb.train(train_set) 
    # TODO save classifier ins a pkl file to be loaded
    return classifier


def get_answer(classifier,sentence):
    #global classifier
    ans = classifier.classify(extract_feature(sentence))
    global answers
    #print answers[ans]
    return ans


def get_word_frequency():
    global faq
    global word_frequency
    for t in faq: 
        question = t[0]
        words = set(question.split(' '))
        for word in words:
            word_frequency[word.lower()] += 1
    return word_frequency

def extract_feature(sentence):
    # TODO define feature extractor
    global word_frequency
    bow = set(sentence.lower().split(' '))
    features = {}
    for word in word_frequency.keys():
        features[word] = (word in bow)
    return features

def get_data(sub_dict,spreadsheetId):
    global offset
    global answers
    global faq
    q = read(spreadsheetId,'pergunta')
    a = read(spreadsheetId,'resposta')
    for row in a:
        answers[int(row[0])+offset] = row[1]    
    for row in q:
        t = (preprocess(row[0],sub_dict),int(row[1])+offset)
        faq += [t]
    offset += 1000


def read_faq(sub_dict):
    global answers
    global faq
    get_data(sub_dict,'1fqDkqnZ1Zws5yrAa7cZryJKZO2hQDrqU2kW64SA8zAo')
    return (faq, answers)
