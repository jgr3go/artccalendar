import google
import datetime
import re
import moment

SHEET_ID='1UaITm4_Con1iuegeSxaT-b8w_cQOK1BwV0ywwGLj_qo'
CAL_ID='bug8mt2ki8cu2ms714euief6q4@group.calendar.google.com'

def main():
  print('Downloading spreadsheet...')

  doc = google.sheets(SHEET_ID)

  races = {}
  raceArr = []

  print('Processing spreadsheet....')
  for sheet in doc.worksheets():
    process_sheet(sheet, races)

  for key in races.keys():
    race = races[key]
    if race['date'] is None or race['date'].date is None:
      print("Warn: '{0}' does not have a date ({1})".format(race['name'], race['rawdate']))
    elif race['date'] < moment.now():
      pass
    else:
      raceArr.append(race)

  raceArr = sorted(raceArr, key=lambda x: x['date'])

  print('Downloading calendar...')
  events = google.getAllCalendarEvents(CAL_ID)
  
  print('Synching...')
  sync(raceArr, events)


def process_sheet(sheet, races):
  matrix = sheet.get_all_values(returnas='matrix')

  for row in matrix:
    if (row[0].strip() != '' and row[0].strip().lower() != 'username'):
      process_row(row, races)


def process_row(row, races):
  racename = safe(row[1])
  if racename == '':
    return

  if racename.lower() not in races:
    races[racename.lower()] = {}
    race = races[racename.lower()]

    race['users'] = []
    race['name'] = safe(row[1])
    race['distance'] = safe(row[3])
    race['city'] = safe(row[5])
    race['state'] = safe(row[6])
    race['start'] = safe(row[7])
    race['date'] = None
    race['rawdate'] = safe(row[4])

    if (race['city'] != '' and race['state'] != ''):
      race['location'] = '{0}, {1}'.format(race['city'], race['state'])
    elif race['city'] != '':
      race['location'] = race['city']
    else:
      race['location'] = race['state']

    date = safe(row[4])
    if date.strip() != '': 
      try:
        d = moment.date(date.strip())
        race['date'] = d 
      except:
        pass



  race = races[racename.lower()]
  race['users'].append(safe(row[0]))



def sync(races, events):
  eventDict = {}
  for event in events:
    eventDict[eventkey(event['date'], safe(event['summary']))] = event 

  for race in races:
    rkey = eventkey(race['date'], race['name'])

    

    if rkey in eventDict:
      event = raceToEvent(race, eventDict[rkey]['id'])
      if diff(event, eventDict[rkey]):
        print('Patching {0}'.format(rkey))
        google.patchEvent(CAL_ID, event['id'], event)
    else:
      event = raceToEvent(race)
      print('Creating {0}'.format(rkey))
      google.createEvent(CAL_ID, event)


def raceToEvent(race, event_id=None):
  event = {
    'summary': race['name'],
    'location': race['location'],
    'start': {
      'date': race['date'].format('YYYY-MM-DD')
    },
    'end': {
      'date': race['date'].add(days=1).format('YYYY-MM-DD')
    },
    'description': '\n'.join(map(lambda u: '/u/'+u, race['users']))
  }
  if event_id is not None:
    event['id'] = event_id

  return event 

def diff(event, gEvent):
  if event['location'] != safe(gEvent['location']):
    return True
  if event['start']['date'] != gEvent['start']['date']:
    return True
  if event['description'] != safe(gEvent['description']):
    return True 

  return False



def safe(st):
  return st.encode('utf-8').strip()
def short(dt):
  return dt.format('YYYY-MM-DD')
def eventkey(date, name):
  return '{0}--{1}'.format(date.format('YYYY-MM-DD'), name.lower())




if __name__ == '__main__':
  main()

