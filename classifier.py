import random
from nltk import FreqDist
from nltk import NaiveBayesClassifier as nb
from nltk.classify import apply_features

def extract_feature(sentence,word_features):
    # TODO define feature extractor
    bow = set(sentence)
    features = {}
    for word in word_features:
        features[word] = (word in bow)
    return features


def create_classifier(documents):
    random.shuffle(documents)
    all_words = FreqDist(w.lower() for w in documents)
    word_features = all_words.keys()[:50]
    train_set = apply_features(document_features, documents[100:])
    test_set = apply_features(document_features, documents[:100])
    classifier = nb.train(train_set) 
    # TODO save classifier ins a pkl file to be loaded
    pass
