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
sub_dict = dict()

def create_classifier():
    global sub_dict
    sub_dict = get_sub_dict(sub_dict,'siglas')
    sub_dict = get_sub_dict(sub_dict,'academico')
    sub_dict = get_sub_dict(sub_dict,'abreviacoes')
    sub_dict = get_sub_dict(sub_dict,'conjuntos')
    read_faq()
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
    global sub_dict
    sentence = preprocess(sentence,sub_dict)
    ans = classifier.classify(extract_feature(sentence))
    global answers
    #print answers[ans]
    return answers[ans]


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

def get_data(spreadsheetId):
    global offset
    global answers
    global faq
    global sub_dict
    q = read(spreadsheetId,'pergunta')
    a = read(spreadsheetId,'resposta')
    for row in a:
        answers[int(row[0])+offset] = row[1]    
    for row in q:
        t = (preprocess(row[0],sub_dict),int(row[1])+offset)
        faq += [t]
    offset += 1000


def read_faq():
    global answers
    global faq
    # colegiado
    get_data('1fqDkqnZ1Zws5yrAa7cZryJKZO2hQDrqU2kW64SA8zAo')
    # apresentacao
    get_data('1IxnEQxrArzEJvoCzdISERzkCEkzM6heVO58FN3F7c9Y')
    # biblioteca
    get_data('1U8t-blzZHM9m1K9H6O1eLYEv_EhuwVUGmrkzcU7STDQ')
    # informacoes_gerais
    get_data('1VXLnbmBo-OBtbFu9JfBSC0v8ufUBTT3sIwpXj5mz8Ec')
    # creditos
    get_data('1FwuOvzxT9pcvuYHIYoYQbByTwNwZWI0NW_WV8_YvPP8')
    # sobre_cursos
    get_data('1z_U7mDvru1dOkhjo62SInosYMzSpXPXBCUVobB7jgFk')
    return (faq, answers)
