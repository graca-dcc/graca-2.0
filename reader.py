import httplib2
import json
import os
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from generate_json import generate_json

def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds']
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('../cred.json', scope)
    cred_json = generate_json()
    credentials = ServiceAccountCredentials._from_parsed_json_keyfile(cred_json,scope)
    return credentials

def read (spreadsheetId, tab):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    rangeName = tab
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    #for row in values:
    #    print('%s, %s' % (row[0], row[1]))
    return values
