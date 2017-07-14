import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
import json
import httplib2
from apiclient import discovery
import datetime
import dateutil.parser as dateparse
import moment

SERVICE_FILE='Reddit-5c99b0f4e099.json'
CALENDAR_SCOPE = 'https://www.googleapis.com/auth/calendar'

_calendarService = None

def sheets(sheetId):
  gc = pygsheets.authorize(service_file=SERVICE_FILE, no_cache=True)

  sheet = gc.open_by_key(sheetId)

  return sheet

def calendar():
  global _calendarService

  if _calendarService is not None:
    return _calendarService

  credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_FILE, CALENDAR_SCOPE)
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http)
  _calendarService = service

  return service


def getAllCalendarEvents(calId):
  calsvc = calendar()

  allEvents = []
  pageToken = None
  start = moment.now().subtract(days=1).datetime.isoformat() + 'Z'

  while True:
    events = calsvc.events().list(calendarId=calId, pageToken=pageToken, timeMin=start).execute()
    for event in events['items']:
      allEvents.append(event)
    pageToken = events.get('nextPageToken')
    if not pageToken:
      break

  fullDayEvents = []
  for event in allEvents:
    start = event['start']
    if 'date' in start:
      event['date'] = moment.date(start['date'])
      fullDayEvents.append(event)
    else:
      # event['dateTime'] = dateparse.parse(start['dateTime'], ignoretz=True)
      # do nothing with these for now
      pass

  fullDayEvents = sorted(fullDayEvents, key=lambda x: x['date'])

  return fullDayEvents

def createEvent(calId, event):
  calsvc = calendar()

  try: 
    event = calsvc.events().insert(calendarId=calId, body=event).execute()
    print('Created {0}'.format(event.get('htmlLink')))
  except Exception as e:
    print(e)

def patchEvent(calId, eventId, event):
  calsvc = calendar()

  try:
    event = calsvc.events().patch(calendarId=calId, eventId=eventId, body=event).execute()
    print('Updated {0}'.format(event.get('htmlLink')))
  except Exception as e:
    print(e)
