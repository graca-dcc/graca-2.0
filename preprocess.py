# -*- coding: utf-8 -*-

import re
import string
from unicodedata import normalize
from reader import read

SUBSTITUTION_SHEET = '1b2uzFDAL8QkidaYKiblU9QcYvovuV4mdPj38GhXLJwk'

def preprocess(sentence):
    sentence = remove_punctuation(sentence)
    sentence = remove_accents(sentence)
    sentence = remove_multiple_spaces(sentence)
    sentence = substitution(sentence)
    sentence = remove_small_words(sentence)
    return sentence


def remove_accents(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')


def remove_punctuation(sentence):
    punctuations = set(string.punctuation)
    sentence = ''.join(ch for ch in sentence if ch not in punctuations)
    return sentence

# TODO maybe a handmade dict with prepositions and articles would be more efficient
def remove_small_words(sentence):
    remover = re.compile(r'\W*\b\w{1,2}\b')
    sentence = remover.sub('', sentence) 
    return sentence


def remove_multiple_spaces(sentence):
    return re.sub( '\s+', ' ', sentence ).strip()


def substitute(sentence,tab):
    data = read(SUBSTITUTION_SHEET,tab)
    for row in data:
        k = row[0]
        value = row[1]
        k = remove_punctuation(k)
        k = remove_multiple_spaces(k)
        k = remove_accents(k)
        value = remove_punctuation(value)
        value = remove_multiple_spaces(value)
        value = remove_accents(value)
        sentence = re.sub( r'\b'+k+r'\b', value, sentence )
    return sentence


def substitution(sentence):
    sentence = substitute(sentence,'siglas')
    sentence = substitute(sentence,'academico')
    sentence = substitute(sentence,'abreviacoes')
    sentence = substitute(sentence,'conjuntos')
    return sentence

