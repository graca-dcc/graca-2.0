import os
import requests
import traceback
import json
from flask import Flask, request
import cPickle as pickle
from classifier import get_answer
from classifier import create_classifier

variaveis = dict()
classifier = pickle.load(open('test_classifier.pickle','rb'))
def get_nome (name, data):
    name = data['entry'][0]['messaging'][0]['sender']['name']
    msg = msg.replace("getNome",name)
    return msg

def substituir_variavel(msg):
    for v in variaveis:
        msg = msg.replace(v,variaveis[v])
    return msg

token = os.environ.get('FB_ACCESS_TOKEN')
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            text = data['entry'][0]['messaging'][0]['message']['text']
            sender = data['entry'][0]['messaging'][0]['sender']['id']
            ans = get_answer(classifier,text)
            payload = {'recipient': {'id': sender}, 'message': {'text': ans}}
            r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET': # Para a verificacao inicial
        if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return 'Nothing'

if __name__ == '__main__':
    app.run(debug=True)
