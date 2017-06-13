# -*- coding: utf-8 -*-

import os
import requests
import traceback
import json
import re
from flask import Flask, request, g
#from classifier import get_answer
#from classifier import create_classifier
from reader import read
import pickle

VARIABLES_SHEET = '176CdCN3k_pRsNYAjw_Tp_l0U9eV-P3kspxLl1gPCmEo'


token = os.environ.get('FB_ACCESS_TOKEN')
app = Flask(__name__)
classifier = pickle.load(open('classifier.pickle','rb'))
variables = pickle.load(open('variables.pickle','rb'))

def get_nome (name, data):
    name = data['entry'][0]['messaging'][0]['sender']['name']
    msg = msg.replace("getNome",name)
    return msg


def substitute_variables(msg):
    global variables
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
            global variables
            ans, prob = classifier.get_answer(text)
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
    app.run(debug=True)
