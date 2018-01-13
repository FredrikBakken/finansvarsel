import sqlite3

from classes import User
from settings import database_connection#, db_encryption, db_decryption


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


#TODO Initialize savings limit account database table
def create_savings_limit_table():
    c = database_connection()

    # Drop table
    sql_cmd_dt = '''DROP TABLE IF EXISTS savings_account_limit'''
    c.execute(sql_cmd_dt)

    # Create table
    sql_cmd_ct = '''CREATE TABLE savings_account_limit(product_id TEXT, bank_id TEXT, bank_name TEXT, bank_url TEXT, bank_region TEXT, bank_account_name TEXT, publication_date TEXT, interest_rate REAL, limit_age INTEGER, PRIMARY KEY(bank_name, bank_account_name))'''
    c.execute(sql_cmd_ct)

    c.close()


# Initialize user database table
def create_user_table():
    print('Creating new user table in the SQLite3 database.')
    c = database_connection()

    sql_cmd_ct = '''CREATE TABLE users(id INTEGER PRIMARY KEY, reg_date TEXT, email TEXT unique, firstname TEXT, lastname TEXT, age TEXT, postal_number TEXT, street_name TEXT, street_number TEXT, phone INTEGER, bsu TEXT, bsu_bank TEXT, savings TEXT, savings_bank TEXT, savings_limit TEXT, savings_limit_bank TEXT, FOREIGN KEY(bsu_bank) REFERENCES bsu(bsu_bank), FOREIGN KEY(savings_bank) REFERENCES savings_account(savings_bank))'''

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


# Insert savings bank data into savings limit database
def insert_savings_limit_account(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age):
    c = database_connection()

    ### Check if account type exist from before
    sql_cmd_exist = c.execute('''SELECT bank_name FROM savings_account_limit WHERE bank_name = ? AND interest_rate = ?''', (bank_name, interest_rate))

    exist = False
    for row in sql_cmd_exist:
        exist = True

    # If it does not exist, insert into database
    if not exist:
        c.execute('''INSERT INTO savings_account_limit(product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age) VALUES (?,?,?,?,?,?,?,?,?)''',
                    (product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age))

    c.commit()
    c.close()


# Insert user into database
def insert_user(usr):
    c = database_connection()
    response = ''

    #local_email = db_encryption(email.encode())
    #print(local_email)

    # New user ==> Insert
    try:
        c.execute('''INSERT INTO users(reg_date, email, firstname, lastname, age, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, savings_limit, savings_limit_bank) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                 (usr.reg_date, usr.email, usr.firstname, usr.lastname, usr.age, usr.postal_number, usr.street_name, usr.street_number, usr.phone, usr.bsu, usr.bsu_bank, usr.savings, usr.savings_bank, usr.savings_limit, usr.savings_limit_bank))
        response = 'new_user'

    # User exist ==> Update
    except sqlite3.IntegrityError:
        c.execute('''UPDATE users SET firstname = ?, lastname = ?, age = ?, postal_number = ?, street_name = ?, street_number = ?, phone = ?, bsu = ?, bsu_bank = ?, savings = ?, savings_bank = ?, savings_limit = ?, savings_limit_bank = ? WHERE email = ?''',
                 (usr.firstname, usr.lastname, usr.age, usr.postal_number, usr.street_name, usr.street_number, usr.phone, usr.bsu, usr.bsu_bank, usr.savings, usr.savings_bank, usr.savings_limit, usr.savings_limit_bank, usr.email))
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
        reg_date            = row[1]
        email               = row[2]
        firstname           = row[3]
        lastname            = row[4]
        age                 = row[5]
        postal_number       = row[6]
        street_name         = row[7]
        street_number       = row[8]
        phone               = row[9]
        bsu                 = row[10]
        bsu_bank            = row[11]
        savings             = row[12]
        savings_bank        = row[13]
        savings_limit       = row[14]
        savings_limit_bank  = row[15]

        current_user = User(reg_date, email, firstname, lastname, age, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, savings_limit, savings_limit_bank)
        user_list.append(current_user)

    c.close()

    return user_list


# Get specific user from database
def get_specific_user(email):
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT * FROM users WHERE email  = ?''', (email,))

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


# Get savings limit banks from database
def get_savings_limit_banks():
    c = database_connection()

    savings_limit_banks = []

    sql_cmd_s = c.execute('''SELECT bank_name, bank_account_name, interest_rate FROM savings_account_limit ORDER BY bank_name ASC''')

    for row in sql_cmd_s:
        bank_name = row[0]
        bank_account_name = row[1]
        #interest_rate = row[2]
        content = bank_name + ' [' + bank_account_name + ']' # + ' %.2f' % interest_rate  # TODO: xx.xx%
        savings_limit_banks.append(content)
    
    c.close()

    return savings_limit_banks



# Get BSU banks with higher interest rates
def get_bsu_banks_with_higher_rates(usr):
    c = database_connection()

    sql_cmd_interest = c.execute('''SELECT interest_rate FROM bsu WHERE bank_name = ?''', (usr.bsu_bank,))

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
def get_savings_account_banks_with_higher_rates(usr):
    c = database_connection()

    sql_cmd_interest = c.execute('''SELECT interest_rate FROM savings_account WHERE bank_name = ?''', (usr.savings_bank,))

    current_rate = 0
    for row in sql_cmd_interest:
        current_rate = row[0]

    sql_cmd_s = c.execute('''SELECT * FROM savings_account WHERE interest_rate > ? ''', (current_rate,))

    results = []
    for row in sql_cmd_s:
        results.append(row)

    c.close()

    return results


# Get savings limit banks with higher interest rates
def get_savings_account_limit_banks_with_higher_rates(usr):
    c = database_connection()

    user_age = usr.age
    bank_name = (usr.savings_limit_bank).split(' [')[0]
    bank_account_name = (usr.savings_limit_bank).split('[')[1].replace('[', '').replace(']', '')

    sql_cmd_interest = c.execute('''SELECT interest_rate FROM savings_account_limit WHERE bank_name = ? AND bank_account_name = ?''', (bank_name, bank_account_name))

    current_rate = 0
    for row in sql_cmd_interest:
        current_rate = row[0]

    if int(user_age) > 34:
        sql_cmd_s = c.execute('''SELECT * FROM savings_account_limit WHERE limit_age = 0 AND interest_rate > ? ''', (current_rate,))
    else:
        sql_cmd_s = c.execute('''SELECT * FROM savings_account_limit WHERE interest_rate > ? ''', (current_rate,))

    results = []
    for row in sql_cmd_s:
        results.append(row)

    c.close()

    return results


# Get user's BSU bank id
def get_user_bsu_bank_id(usr):
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT bank_id FROM bsu WHERE bank_name = ?''', (usr.bsu_bank,))

    id = ''
    for row in sql_cmd_s:
        id = row[0]

    c.close()

    return id


# Get user's savings account bank id
def get_user_savings_bank_id(usr):
    c = database_connection()

    sql_cmd_s = c.execute('''SELECT bank_id FROM savings_account WHERE bank_name = ?''', (usr.savings_bank,))

    id = ''
    for row in sql_cmd_s:
        id = row[0]

    c.close()

    return id


# Get user's savings account limit bank id ISSUES
def get_user_savings_limit_bank_id(usr):
    c = database_connection()

    bank_name = (usr.savings_limit_bank).split(' [')[0]

    sql_cmd_s = c.execute('''SELECT bank_id FROM savings_account_limit WHERE bank_name = ?''', (bank_name,))

    id = ''
    for row in sql_cmd_s:
        id = row[0]

    c.close()

    return id

