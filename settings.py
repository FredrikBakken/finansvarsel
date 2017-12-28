import json
import gspread
import sqlite3

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Centralized global variables

### Change Bank URL
url_change_bank = 'https://www.finansportalen.no/bank/bankbytte/'

### BSU Banks URL
bsu_count = 2
url_bsu_regions = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=1&alderstilbudAr=24&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&kraft_sparekonto_med_spareavtale=ja&kraft_sparekonto_uten_spareavtale=ja&bsu=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'
url_bsu_country = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=1&alderstilbudAr=24&nasjonalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&kraft_sparekonto_med_spareavtale=ja&kraft_sparekonto_uten_spareavtale=ja&bsu=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'

### Bank Savings URL
# INSERT URLS

# Centralized data extraction methods

### Get current time method
def time_now(time_variable):
    t = ''

    # Setting time/date format
    if time_variable == 'date.month.year':
        t = datetime.now().strftime('%d.%m.%Y')

    return t


### Spreadsheet client login
def access_spreadsheet():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    client.login()
    sheet = client.open('finans-notifier-spreadsheet')
    return sheet


### Open database connectivity
def database_connection():
    connection = sqlite3.connect('database/db.db')
    return connection


### Check and set codec exceptions
def check_codec(v):
    variable = v

    if b"\xf8" in variable:
        variable = variable.replace(b'\xf8', b'o')
    elif b"\xd8" in variable:
        variable = variable.replace(b'\xd8', b'O')
    elif b"\xe5" in variable:
        variable = variable.replace(b'\xe5', b'a')
    elif b"\xe6" in variable:
        variable = variable.replace(b'\xe6', b'ae')

    return variable


### Get email credentials from secrets file
def email_credentials():
    jdata = json.loads(open('secrets.json').read())
    username = jdata['email-username']
    password = jdata['email-password']

    return username, password
