import httplib2
import json
import os
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds']
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('../cred.json', scope)
    cred_json = json.loads(os.environ.get('CRED_JSON'))
    credentials = ServiceAccountCredentials.from_json(cred_json, scope)
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
