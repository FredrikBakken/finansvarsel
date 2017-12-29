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


# Initialize savings account database table
def create_savings_table():
    c = database_connection()

    # Drop table
    sql_cmd_dt = '''DROP TABLE IF EXISTS savings_account'''
    c.execute(sql_cmd_dt)

    # Create table
    sql_cmd_ct = '''CREATE TABLE savings_account(product_id TEXT, bank_id TEXT, bank_name TEXT, bank_url TEXT, bank_region TEXT, bank_account_name TEXT, publication_date TEXT, interest_rate REAL, PRIMARY KEY(bank_name))'''
    c.execute(sql_cmd_ct)

    c.close()


# Initialize user database table
def create_user_table():
    print('Creating new user table in the SQLite3 database.')
    c = database_connection()

    sql_cmd_ct = '''CREATE TABLE users(id INTEGER PRIMARY KEY, email TEXT unique, firstname TEXT, lastname TEXT, postal_number INTEGER, street_name TEXT, street_number TEXT, phone INTEGER, bsu TEXT, bsu_bank TEXT, savings TEXT, savings_bank TEXT, FOREIGN KEY(bsu_bank) REFERENCES bsu(bsu_bank), FOREIGN KEY(savings_bank) REFERENCES savings_account(savings_bank))'''

    try:
        c.execute(sql_cmd_ct)
    except sqlite3.OperationalError:
        print('User table already exists, execution continues...')

    c.close()


# Initialize inactive users database table
def inactive_user_table():
    c = database_connection()

    sql_cmd_ct = '''CREATE TABLE inactive_users(id INTEGER PRIMARY KEY, email TEXT, reason TEXT)'''

    try:
        c.execute(sql_cmd_ct)
    except sqlite3.OperationalError:
        print('Inactive user table already exists, execution continues...')

    c.close()


########################################################################################################################
########################################################################################################################

# Insert BSU bank data into BSU database
def insert_bsu(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate):
    c = database_connection()

    c.execute('''INSERT INTO bsu(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate) VALUES (?,?,?,?,?,?,?,?)''',
             (product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate))
    c.commit()

    c.close()


# Insert savings bank data into savings database
def insert_savings_account(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate):
    c = database_connection()

    c.execute('''INSERT INTO savings_account(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate) VALUES (?,?,?,?,?,?,?,?)''',
             (product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate))
    c.commit()

    c.close()


# Insert user into database
def insert_user(email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank):
    c = database_connection()
    response = ''

    # New user ==> Insert
    try:
        c.execute('''INSERT INTO users(email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                 (email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank))
        response = 'new_user'

    # User exist ==> Update
    except sqlite3.IntegrityError:
        c.execute('''UPDATE users SET firstname = ?, lastname = ?, postal_number = ?, street_name = ?, street_number = ?, phone = ?, bsu = ?, bsu_bank = ?, savings = ?, savings_bank = ? WHERE email = ?''',
                 (firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, email))
        response = 'update_user'

    c.commit()

    c.close()

    return response


########################################################################################################################
########################################################################################################################

# Delete user from database
def delete_user(email, reason, store):
    c = database_connection()

    try:
        c.execute('''DELETE FROM users WHERE email = ?''', (email,))
    except sqlite3.IntegrityError:
        print('The user does not exist in the database, execution continues...')

    if store == "Ja":
        c.execute('''INSERT INTO inactive_users(email, reason) VALUES (?,?)''', (email, reason))
    else:
        c.execute('''INSERT INTO inactive_users(reason) VALUES (?)''', (reason,))

    c.commit()

    c.close()


########################################################################################################################
########################################################################################################################

# Get users from database
def get_all_users():
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT * FROM users''')

    user_list = []
    for row in sql_cmd_s:
        user_list.append(row)

    c.close()

    return user_list


# Get BSU banks from database
def get_bsu_banks():
    c = database_connection()

    bsu_banks = []

    sql_cmd_s = c.execute('''SELECT bank_name FROM bsu ORDER BY bank_name ASC''')

    for row in sql_cmd_s:
        bsu_banks.append(row[0])

    c.close()

    return bsu_banks

# Get savings banks from database
def get_savings_banks():
    c = database_connection()

    savings_banks = []

    sql_cmd_s = c.execute('''SELECT bank_name FROM savings_account ORDER BY bank_name ASC''')

    for row in sql_cmd_s:
        savings_banks.append(row[0])

    c.close()

    return savings_banks


# Get BSU banks with higher interest rates
def get_bsu_banks_with_higher_rates(user):
    c = database_connection()

    sql_cmd_interest = c.execute('''SELECT interest_rate FROM bsu WHERE bank_name = ?''', (user[9],))

    current_rate = 0
    for row in sql_cmd_interest:
        current_rate = row[0]

    sql_cmd_s = c.execute('''SELECT * FROM bsu WHERE interest_rate > ? ''', (current_rate,))

    results = []
    for row in sql_cmd_s:
        results.append(row)

    c.close()

    return results


# Get savings banks with higher interest rates
def get_savings_account_banks_with_higher_rates(user):
    c = database_connection()

    sql_cmd_interest = c.execute('''SELECT interest_rate FROM savings_account WHERE bank_name = ?''', (user[11],))

    current_rate = 0
    for row in sql_cmd_interest:
        current_rate = row[0]

    sql_cmd_s = c.execute('''SELECT * FROM savings_account WHERE interest_rate > ? ''', (current_rate,))

    results = []
    for row in sql_cmd_s:
        results.append(row)

    c.close()

    return results


# Get user's BSU bank id
def get_user_bsu_bank_id(user):
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT bank_id FROM bsu WHERE bank_name = ?''', (user[9],))

    id = ''
    for row in sql_cmd_s:
        id = row[0]

    return id


# Get user's savings account bank id
def get_user_savings_bank_id(user):
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT bank_id FROM savings_account WHERE bank_name = ?''', (user[11],))

    id = ''
    for row in sql_cmd_s:
        id = row[0]

    return id
