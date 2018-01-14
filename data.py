import re
import os
import openpyxl as opxl
import requests
import contextlib

from classes import Saving

from db import create_saving_table, insert_savings_data, get_saving_banks

from settings import access_spreadsheet, url_bsu_regions, url_bsu_country, url_savings_acc_nolimit, url_savings_acc_limit_34less, url_savings_acc_limit_34more, url_retirement_savings, url_usage_and_salary, check_codec, time_now


# Method for downloading finansportalen content
def download_content(url, filename):
    if not os.path.exists('download'):
        os.makedirs('download')

    response = requests.get(url)
    with open(os.path.join('download', filename), 'wb') as f:
        f.write(response.content)


# Method for extracting column data from file
def extract_xlsx_data(file):
    data = []

    # Load file
    wb = opxl.load_workbook('download/' + file)

    # Open worksheet
    work_sheet = time_now('date.month.year')
    ws = wb.get_sheet_by_name(work_sheet)

    # Read specific columns row by row contents from file
    for row in range(2, ws.max_row + 1):
        data_item = []
        for column in "BLOMPDEH":
            cell_name = "{}{}".format(column, row)
            cell_data = ws[cell_name].value
            data_item.append(cell_data)

        data.append(data_item)

    # Delete temporary file downloaded
    with contextlib.suppress(FileNotFoundError):
        os.remove('download/' + file)

    return data


# Method for updating Google form data
def update_form(banks, sheet_number):
    # Initialize spreadsheet and worksheet
    sheet = access_spreadsheet()
    bank_sheet = sheet.get_worksheet(sheet_number)
    row = 3
    after_row = (len(banks) + 3)

    # Insert all data into sheet
    print('Adding banks to form.')
    for x in range(len(banks)):
        bank_sheet.update_acell('A%s' % (row), banks[x])
        row += 1

    # Deleting all banks that are no longer represented
    print('Deleting old banks from form.')
    while True:
        next_cell = bank_sheet.acell('A%s' % (after_row))

        if not next_cell.value == '':
            bank_sheet.update_acell('A%s' % (after_row), '')
        else:
            break

        after_row += 1


# Method for handling and storing extracted data
def handle_and_store_data(savings_data, account_type, limit_age):
    account_type = account_type
    product_id = ''
    bank_id = ''
    bank_name = ''
    bank_url = ''
    bank_region = ''
    bank_account_name = ''
    publication_date = ''
    interest_rate = ''
    limit_age = limit_age

    # Loop through rows in Excel file
    for x in range(len(savings_data)):
        product_id = str(int(savings_data[x][0])).strip()
        bank_id = str(int(savings_data[x][1])).strip()

        bank_name = savings_data[x][2].encode('ISO-8859-1', 'ignore')
        bank_name = check_codec(bank_name).decode('ISO-8859-1').strip()

        bank_url = savings_data[x][3]
        if 'http:' in bank_url:
            bank_url = bank_url.replace('http:', 'https:').strip()  # For security reasons

        bank_region = savings_data[x][4].strip()
        bank_account_name = savings_data[x][5].strip()
        publication_date = savings_data[x][6].strip()
        interest_rate = float("%.2f" % savings_data[x][7])

        # Create saving account object
        current_row = Saving(account_type, product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age)

        # Insert saving data into database
        insert_savings_data(current_row)


# Method for handling all savings account data
def get_savings_data(account_types):
    account_data = [                                        # [account_type, filename, url, limit_age]
        ['bsu', 'bsu_regions.xlsx', url_bsu_regions, ''],
        ['bsu', 'bsu_country.xlsx', url_bsu_country, ''],
        ['savings_nolimit', 'savings_account_nolimit.xlsx', url_savings_acc_nolimit, ''],
        ['savings_limit', 'savings_account_limit_34h.xlsx', url_savings_acc_limit_34more, '0'],
        ['savings_limit', 'savings_account_limit_34l.xlsx', url_savings_acc_limit_34less, '1'],
        ['retirement', 'retirement_saving.xlsx', url_retirement_savings, ''],
        ['usage_salary', 'usage_and_salary.xlsx', url_usage_and_salary, '']
    ]

    # Reset savings database table
    create_saving_table()

    # Loop through the data content
    for x in range(len(account_data)):
        account_type = account_data[x][0]
        filename = account_data[x][1]
        url = account_data[x][2]
        limit_age = account_data[x][3]

        # Data variable
        savings_data = []

        # Download data content
        download_content(url, filename)

        # Extract data from .xlsx file
        savings_data = extract_xlsx_data(filename)

        # Handle and store extracted data
        handle_and_store_data(savings_data, account_type, limit_age)
    
    # Loop through the stored savings data and update Google Form
    for x in range(len(account_types)):
        account_type = account_types[x][0]
        worksheet_page = account_types[x][1]

        # Get banks for current bank type
        current_banks = get_saving_banks(account_type)

        # Store banks to correct worksheet page
        update_form(current_banks, worksheet_page)
