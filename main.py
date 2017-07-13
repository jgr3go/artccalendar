import google

SHEET_ID='1UaITm4_Con1iuegeSxaT-b8w_cQOK1BwV0ywwGLj_qo'
CAL_ID='bug8mt2ki8cu2ms714euief6q4@group.calendar.google.com'

def main():
  print('Downloading spreadsheet...')

  doc = google.sheets(SHEET_ID)

  races = {}

  for sheet in doc.worksheets():
    process_sheet(sheet, races)

  calSvc = google.calendar()

  



def process_sheet(sheet, races):
  matrix = sheet.get_all_values(returnas='matrix')

  for row in matrix:
    if (row[0].strip() != '' and row[0].strip().lower() != 'username'):
      process_row(row, races)


def process_row(row, races):
  racename = row[1]
  if racename.lower() not in races:
    races[racename.lower()] = {}
    race = races[racename.lower()]

    race['users'] = []
    race['name'] = row[1]
    race['distance'] = row[3]
    race['date'] = row[4]
    race['city'] = row[5]
    race['state'] = row[6]
    race['start'] = row[7]

  race = races[racename.lower()]
  race['users'].append(row[0])




if __name__ == '__main__':
  main()

