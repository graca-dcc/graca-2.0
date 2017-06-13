# -*- coding: utf-8 -*-

import re
import string
from unicodedata import normalize
import unicodedata
from reader import read

SUBSTITUTION_SHEET = '1b2uzFDAL8QkidaYKiblU9QcYvovuV4mdPj38GhXLJwk'

def preprocess(sentence, sub_dict):
    sentence = remove_punctuation(sentence)
    sentence = remove_accents(sentence)
    sentence = remove_multiple_spaces(sentence)
    sentence = substitution(sentence, sub_dict)
    sentence = remove_small_words(sentence)
    sentence = remove_multiple_spaces(sentence)
    return sentence


def remove_accents(sentence, codif='utf-8'):
    try:
        nfkd = unicodedata.normalize('NFKD', sentence)
        sentence = u"".join([c for c in nfkd if not unicodedata.combining(c)])
        return re.sub('[^a-zA-Z0-9 \\\]', '', sentence)
    except TypeError:
        return normalize('NFKD', sentence.decode(codif)).encode('ASCII','ignore')
    return sentence

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


def substitute(sentence,sub_dict,tab):
    data = sub_dict[tab]
    for k in data:
        sentence = re.sub( r'\b'+k+r'\b', data[k], sentence )
    return sentence


def substitution(sentence,sub_dict):
    sentence = substitute(sentence, sub_dict, 'siglas')
    sentence = substitute(sentence, sub_dict, 'academico')
    sentence = substitute(sentence, sub_dict, 'abreviacoes')
    sentence = substitute(sentence, sub_dict, 'conjuntos')
    return sentence


def get_sub_dict(sub_dict,tab):
    data = read(SUBSTITUTION_SHEET,tab)
    aux_dict = dict()
    for row in data:
        k = row[0]
        value = row[1]
        k = remove_punctuation(k)
        k = remove_multiple_spaces(k)
        k = remove_accents(k)
        value = remove_punctuation(value)
        value = remove_multiple_spaces(value)
        value = remove_accents(value)
        aux_dict[k] = value
    sub_dict[tab] = aux_dict
    return sub_dict
