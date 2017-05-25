import re
import string

def remove_punctuation(sentence):
    punctuations = set(string.punctuation)
    sentence = ''.join(ch for ch in sentence if ch not in punctuations)
    return sentence


def remove_multiple_spaces(sentence):
    return re.sub( '\s+', ' ', sentence ).strip()


def substitution(sentence):
    # TODO substitute words
    return sentence


# TODO maybe a handmade dict with pronouns and articles would be more efficient
def remove_small_words(sentence):
    remover = re.compile(r'\W*\b\w{1,2}\b'} 
    return sentence


def preprocess(sentence):
    remove_punctuation(sentence)
    remove_multiple_spaces(sentence)
    substitution(sentence)
    remove_small_words(sentence)
    return sentence
