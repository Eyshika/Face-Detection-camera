import json
import sys
import time
import datetime
import gspread
import psutil
import subprocess
from system_info import get_temperature
from oauth2client.service_account import ServiceAccountCredentials
GDOCS_OAUTH_JSON       = 'rpidata-bd77a066019d.json'
GDOCS_SPREADSHEET_NAME = 'Rpi_data'
FREQUENCY_SECONDS      = 20
def login_open_sheet(oauth_key_file, spreadsheet):
	try:
		credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, 
										scopes=['https://spreadsheets.google.com/feeds'])
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print 'Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!'
		print 'Google sheet login failed with error:', ex
		sys.exit(1)
print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None
while True:
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        dat = datetime.datetime.now()
	cpu = psutil.cpu_percent()
        tmp = get_temperature()
        print(dat)
        print('CPU Usage in %: '+str(cpu))
        print('Temperature in C: ' +str(tmp))
	try:
		worksheet.append_row((dat, cpu, tmp))
	except:
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue
	print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)
