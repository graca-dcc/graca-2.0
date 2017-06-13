# -*- coding: utf-8 -*-
import pickle
import re

variables = pickle.load(open('variables.pickle', 'rb'))
cls = pickle.load(open('classifier.pickle', 'rb'))


def substitute_variables(msg):
    for v in variables:
        msg = re.sub(r'\b'+v+r'\b',variables[v], msg)
    return msg


while True:
    pergunta = raw_input('Pergunta: ')
    import pdb; pdb.set_trace()
    ans, prob = cls.get_answer(pergunta)
    print 'Resposta: '+substitute_variables(ans)
    print prob
