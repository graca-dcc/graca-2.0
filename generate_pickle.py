from classifier import Classifier
from reader import read
import re
import pickle

VARIABLES_SHEET = '176CdCN3k_pRsNYAjw_Tp_l0U9eV-P3kspxLl1gPCmEo'

def load_variables():
    variables = dict()
    data = read(VARIABLES_SHEET, 'colegiado')
    for row in data:
        k = row[0]
        value = row[1]
        variables['var_'+k] = value
    return variables

variables = load_variables()
pickle.dump(variables, open('variables.pickle', 'wb'))
cls = Classifier()
cls.save_classifier()
