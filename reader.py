import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


offset = 100

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('../cred.json', scope)
    return credentials

def read (spreadsheetId):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    rangeName = 'pergunta'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    #for row in values:
    #    print('%s, %s' % (row[0], row[1]))
    return values
