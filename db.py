import sqlite3

from settings import database_connection


########################################################################################################################
########################################################################################################################

# Initialize BSU database table
def create_bsu_table():
    c = database_connection()

    # Drop table
    sql_cmd_dt = '''DROP TABLE IF EXISTS bsu'''
    c.execute(sql_cmd_dt)

    # Create table
    sql_cmd_ct = '''CREATE TABLE bsu(product_id TEXT, bank_id TEXT, bank_name TEXT, bank_url TEXT, bank_region TEXT, bank_account_name TEXT, publication_date TEXT, interest_rate REAL, PRIMARY KEY(bank_name))'''
    c.execute(sql_cmd_ct)

    c.close()


# Initialize user database table
def create_user_table():
    print('Creating new user table in the SQLite3 database.')
    c = database_connection()

    sql_cmd_ct = '''CREATE TABLE users(id INTEGER PRIMARY KEY, email TEXT unique, firstname TEXT, lastname TEXT, postal_number INTEGER, street_name TEXT, street_number TEXT, phone INTEGER, bsu TEXT, bsu_bank TEXT, FOREIGN KEY(bsu_bank) REFERENCES bsu(bsu_bank))'''

    try:
        c.execute(sql_cmd_ct)
    except sqlite3.OperationalError:
        print('User table already exists, execution continues...')

    c.close()


########################################################################################################################
########################################################################################################################

# Insert BSU bank data into BSU database
def insert_bsu(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate):
    c = database_connection()

    c.execute('''INSERT INTO bsu(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate) VALUES (?,?,?,?,?,?,?,?)''', (product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate))
    c.commit()

    c.close()


# Insert user into database
def insert_user(email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank):
    c = database_connection()
    response = ''

    # New user ==> Insert
    try:
        c.execute('''INSERT INTO users(email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank) VALUES (?,?,?,?,?,?,?,?,?)''', (email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank))
        response = 'new_user'

    # User exist ==> Update
    except sqlite3.IntegrityError:
        c.execute('''UPDATE users SET firstname = ?, lastname = ?, postal_number = ?, street_name = ?, street_number = ?, phone = ?, bsu = ?, bsu_bank = ? WHERE email = ?''', (firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank, email))
        response = 'update_user'

    c.commit()

    c.close()

    return response


########################################################################################################################
########################################################################################################################
# TODO! DELETE USER DATA
# Delete user from database
def delete_user(email, reason, store):
    c = database_connection()

    return True


########################################################################################################################
########################################################################################################################

# Get users' current BSU bank data
def get_users_current_bsu_bank():
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT users.firstname, users.lastname, users.email, users.postal_number, users.street_name, users.street_number, users.phone, users.bsu_bank, bsu.bank_id, bsu.interest_rate FROM users, bsu WHERE users.bsu_bank = bsu.bank_name''')

    data = []
    for row in sql_cmd_s:
        data.append(row)

    c.close()

    return data


# Get BSU database contents
def get_bsu_content():
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT * FROM bsu''')

    for row in sql_cmd_s:
        print(row)

    c.close()


# Get BSU banks from database
def get_bsu_banks():
    c = database_connection()

    bsu_banks = []

    sql_cmd_s = c.execute('''SELECT bank_name FROM bsu ORDER BY bank_name ASC''')

    for row in sql_cmd_s:
        bsu_banks.append(row[0])

    c.close()

    return bsu_banks


# Get BSU bank rates
def get_bsu_rates(bank_name):
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT interest_rate FROM bsu WHERE bank_name=?''', (bank_name,))

    interest_rate = sql_cmd_s.fetchone()[0]

    c.close()

    return interest_rate


# Get BSU banks with higher interest rates
def get_banks_with_higher_rates(user):
    c = database_connection()

    results = []

    sql_cmd_s = c.execute('''SELECT * FROM bsu WHERE interest_rate > ? ''', (user[9],))

    for row in sql_cmd_s:
        results.append(row)

    c.close()

    return results
