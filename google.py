import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import json
import httplib2
from apiclient import discovery

SERVICE_FILE='Reddit-5c99b0f4e099.json'
CALENDAR_SCOPE = 'https://www.googleapis.com/auth/calendar'

def sheets(sheetId):
  gc = pygsheets.authorize(service_file=SERVICE_FILE, no_cache=True)

  sheet = gc.open_by_key(sheetId)

  return sheet

def calendar(calId):

  credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_FILE, CALENDAR_SCOPE)
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http)

  return service
