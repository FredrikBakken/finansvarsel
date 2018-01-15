import os
import sys
import json
import gspread
import sqlite3

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


# Centralized global variables

### Change Bank URL
url_change_bank = 'https://www.finansportalen.no/bank/bankbytte/'

### BSU Banks URL
url_bsu_regions = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=1&alderstilbudAr=24&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&kraft_sparekonto_med_spareavtale=ja&kraft_sparekonto_uten_spareavtale=ja&bsu=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'
url_bsu_country = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=1&alderstilbudAr=24&nasjonalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&kraft_sparekonto_med_spareavtale=ja&kraft_sparekonto_uten_spareavtale=ja&bsu=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'

### Bank Savings URL
url_savings_acc_nolimit = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=90000&alderstilbudAr=21&nasjonalt=ja&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&all=ja&sparekonto_uten_begrensninger=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'
url_savings_acc_limit_34less = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=50000&alderstilbudAr=30&nasjonalt=ja&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&all=ja&sparekonto_med_begrensninger=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'
url_savings_acc_limit_34more = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=50000&alderstilbudAr=36&nasjonalt=ja&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&all=ja&sparekonto_med_begrensninger=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'

### Retirement Bank URL
url_retirement_savings = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=50000&alderstilbudAr=40&nasjonalt=ja&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&all=ja&pensjonssparing=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'

### Use/Salary Bank URL
url_usage_and_salary = 'https://www.finansportalen.no/services/kalkulator/banksparing/export?kalkulatortype=banksparing&totalt_innestaende=50000&alderstilbudAr=40&nasjonalt=ja&regionalt=ja&visUtenProduktpakker=ja&neiforutsettermedlemskap=ja&all=ja&brukskonto=ja&sortcolumn=effectiveInterestRate%2C-bank.name%2C-name&sortdirection=desc'



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
    if not os.path.exists('database'):
        os.makedirs('database')

    connection = sqlite3.connect('database/db.db')
    return connection


### Get credentials from secrets file
def credentials():
    jdata = json.loads(open('secrets.json').read())
    username = jdata['email-username']
    password = jdata['email-password']
    server_port = jdata['email-server']

    return username, password, server_port
