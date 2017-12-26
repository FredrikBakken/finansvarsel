import os
import openpyxl as opxl
import requests
import contextlib

from db import create_bsu_table, insert_bsu, get_bsu_banks, get_bsu_content

from settings import access_spreadsheet, bsu_count, url_bsu_regions, url_bsu_country, check_codec, time_now


# Method for downloading finansportalen content
def download_content(url, filename):
    response = requests.get(url)
    with open(os.path.join('download', filename), 'wb') as f:
        f.write(response.content)


# Method for handling BSU data
def get_bsu_data():
    bsu_files = ['bsu_regions.xlsx', 'bsu_country.xlsx']
    bsu_urls = [url_bsu_regions, url_bsu_country]

    # Reset BSU database table
    create_bsu_table()

    # Looping through the data content
    for x in range(bsu_count):
        bsu_data = []

        # Setting local bsu variables
        bsu_file = bsu_files[x]
        bsu_url = bsu_urls[x]

        # Download data content
        download_content(bsu_url, bsu_file)

        # Load file
        wb = opxl.load_workbook('download/' + bsu_file)

        # Open worksheet
        work_sheet = time_now('date.month.year')
        ws = wb.get_sheet_by_name(work_sheet)

        # Read specific columns row by row contents from file
        for row in range(2, ws.max_row + 1):
            bsu_data_item = []
            for column in "BOMPDEH":
                cell_name = "{}{}".format(column, row)
                cell_data = ws[cell_name].value
                bsu_data_item.append(cell_data)

            bsu_data.append(bsu_data_item)

        # Delete temporary file downloaded
        with contextlib.suppress(FileNotFoundError):
            os.remove('download/' + bsu_file)

        # Reset variables
        product_id = ''
        bank_name = ''
        bank_url = ''
        bank_region = ''
        bank_account_name = ''
        publication_date = ''
        interest_rate = ''

        # Loop through rows in Excel file
        for y in range(len(bsu_data)):
            product_id = str(int(bsu_data[y][0]))

            bank_name = bsu_data[y][1].encode('ISO-8859-1', 'ignore')
            bank_name = check_codec(bank_name).decode('ISO-8859-1')

            bank_url = bsu_data[y][2]
            if 'http:' in bank_url:
                bank_url = bank_url.replace('http:', 'https:')  # For security reasons

            bank_region = bsu_data[y][3]
            bank_account_name = bsu_data[y][4]
            publication_date = bsu_data[y][5]
            interest_rate = str("%.2f" % bsu_data[y][6])

            # Insert bsu data into database
            insert_bsu(product_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate)

    get_bsu_content()


    print('Start Google Spreadsheet handling for BSU data.')

    # Get BSU bank names from BSU database
    bsu_banks = get_bsu_banks()

    # Initialize spreadsheet and worksheet
    sheet = access_spreadsheet()
    bsu_bank_sheet = sheet.get_worksheet(1)
    row = 3
    after_row = (len(bsu_banks) + 3)

    # Insert all data into sheet
    for x in range(len(bsu_banks)):
        bsu_bank_sheet.update_acell('A%s' % (row), bsu_banks[x])
        row += 1

    # Deleting all banks that are no longer represented
    for x in range(1000):
        next_cell = bsu_bank_sheet.acell('A%s' % (after_row))

        if not next_cell.value == '':
            bsu_bank_sheet.update_acell('A%s' % (after_row), '')
        else:
            break

        after_row += 1





# Method for handling savings data (Placeholder)
def get_savings_data():
    return True