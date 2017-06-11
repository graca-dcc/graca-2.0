import random
from nltk import FreqDist
from nltk import NaiveBayesClassifier as nb
from nltk.classify import apply_features
from reader import read
from preprocess import preprocess
from preprocess import get_sub_dict

def create_classifier(documents):
    random.shuffle(documents)
    all_words = FreqDist(w.lower() for w in documents)
    word_features = all_words.keys()[:50]
    train_set = apply_features(document_features, documents[100:])
    test_set = apply_features(document_features, documents[:100])
    classifier = nb.train(train_set) 
    # TODO save classifier ins a pkl file to be loaded
    pass


def extract_feature(sentence,word_features):
    # TODO define feature extractor
    bow = set(sentence)
    features = {}
    for word in word_features:
        features[word] = (word in bow)
    return features

offset = 1000
answers = dict()
faq = []
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
