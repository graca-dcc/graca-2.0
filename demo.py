# -*- coding: utf-8 -*-

#from preprocess import preprocess

#msg = 'vc é muito linda. te conheço do DA de si, não é?'

#print (preprocess(msg))

import pdb
from nltk import FreqDist
from preprocess import get_sub_dict
from classifier import read_faq
from classifier import get_word_frequency
"""
subdict = dict()
subdict = get_sub_dict(subdict,'siglas')
subdict = get_sub_dict(subdict,'academico')
subdict = get_sub_dict(subdict,'abreviacoes')
subdict = get_sub_dict(subdict,'conjuntos')
q, a = read_faq(subdict)
wf = get_word_frequency()
pdb.set_trace()
"""
from classifier import create_classifier
from classifier import get_answer
classifier = create_classifier()
import cPickle as pickle
pickle.dump(classifier, open('test_classifier.pickle', 'wb'))
cl = pickle.load(open('test_classifier.pickle','rb'))
pergunta = 'qual o telefone do colegiado de ciencia da computação?'
get_answer(cl,pergunta)
