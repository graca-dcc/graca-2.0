# -*- coding: utf-8 -*-

from classifier import create_classifier
from classifier import get_answer
from reader import read
import re

VARIABLES_SHEET = '176CdCN3k_pRsNYAjw_Tp_l0U9eV-P3kspxLl1gPCmEo'

def load_variables():
    variables = dict()
    data = read(VARIABLES_SHEET, 'colegiado')
    for row in data:
        k = row[0]
        value = row[1]
        variables['var_'+k] = value
    return variables

classifier = create_classifier()
variables = load_variables()


def substitute_variables(msg):
    for v in variables:
        msg = re.sub(r'\b'+v+r'\b',variables[v], msg)
    return msg

classifier = create_classifier()
#pergunta = 'qual o telefone do colegiado de ciencia da computação?'
pergunta = 'bom dia graça, preciso do email do colegiado de matematica computacional'
ans = get_answer(classifier,pergunta)
print substitute_variables(ans)
