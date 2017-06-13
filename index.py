# -*- coding: utf-8 -*-

import os
import requests
import traceback
import json
import re
from flask import Flask, request
from classifier import get_answer
from classifier import create_classifier
from reader import read

VARIABLES_SHEET = '176CdCN3k_pRsNYAjw_Tp_l0U9eV-P3kspxLl1gPCmEo'


token = os.environ.get('FB_ACCESS_TOKEN')
app = Flask(__name__)
#classifier = create_classifier()
#import cPickle as pickle
#classifier = pickle.load(open('classifier.pickle','rb'))
#answers = pickle.load(open('answers.pickle','rb'))
#sub_dict = pickle.load(open('sub_dict.pickle','rb'))
#from sklearn.externals import joblib
#answers = joblib.load('ans.pkl')
#classifier = joblib.load('cls.pkl')
#sub_dict = joblib.load('sd.pkl')

def load_variables():
    variables = dict()
    data = read(VARIABLES_SHEET, 'colegiado')
    for row in data:
        k = row[0]
        value = row[1]
        variables['var_'+k] = value
    return variables




def get_nome (name, data):
    name = data['entry'][0]['messaging'][0]['sender']['name']
    msg = msg.replace("getNome",name)
    return msg


def substitute_variables(msg):
    for v in variables:
        msg = re.sub(r'\b'+v+r'\b',variables[v],msg)
    return msg


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            text = data['entry'][0]['messaging'][0]['message']['text']
            sender = data['entry'][0]['messaging'][0]['sender']['id']
            global classifier
            ans = get_answer(classifier,answers,sub_dict,text)
            ans = substitute_variables(ans)
            payload = {'recipient': {'id': sender}, 'message': {'text': ans}}
            r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return 'Nothing'

if __name__ == '__main__':
    variables = load_variables()
    classifier, answers, sub_dict = create_classifier()
    app.run(debug=True)
