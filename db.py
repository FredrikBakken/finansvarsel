import sqlite3

from classes import User, Saving
from settings import database_connection#, db_encryption, db_decryption


########################################################################################################################
########################################################################################################################

# Initialize the saving banks database table
def create_saving_table():
    c = database_connection()

    # Drop table
    sql_cmd_dt = '''DROP TABLE IF EXISTS saving'''
    c.execute(sql_cmd_dt)

    # Create table
    sql_cmd_ct = '''CREATE TABLE saving(account_type TEXT, product_id TEXT, bank_id TEXT, bank_name TEXT, bank_url TEXT, bank_region TEXT, bank_account_name TEXT, publication_date TEXT, interest_rate REAL, limit_age INTEGER, PRIMARY KEY(account_type, bank_name, bank_account_name))'''
    c.execute(sql_cmd_ct)

    c.close()


# Initialize user database table
def create_user_table():
    print('Creating new user table in the SQLite3 database.')
    c = database_connection()

    sql_cmd_ct = '''CREATE TABLE users(id INTEGER PRIMARY KEY, reg_date TEXT, email TEXT unique, firstname TEXT, lastname TEXT, age TEXT, postal_number TEXT, street_name TEXT, street_number TEXT, phone INTEGER, bsu TEXT, bsu_bank TEXT, savings TEXT, savings_bank TEXT, savings_limit TEXT, savings_limit_bank TEXT, retirement TEXT, retirement_bank TEXT, usagesalary TEXT, usagesalary_bank TEXT)'''

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

# Insert Saving object into database
def insert_savings_data(saving):
    c = database_connection()

    ### Check if account type exist from before
    sql_cmd_exist = c.execute('''SELECT bank_name FROM saving WHERE bank_name = ? AND bank_account_name = ?''', (saving.bank_name, saving.bank_account_name))

    exist = False
    for row in sql_cmd_exist:
        exist = True

    # If it does not exist, insert into database
    if not exist:
        c.execute('''INSERT INTO saving(account_type, product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                 (saving.account_type, saving.product_id, saving.bank_id, saving.bank_name, saving.bank_url, saving.bank_region, saving.bank_account_name, saving.publication_date, saving.interest_rate, saving.limit_age))
    c.commit()
    c.close()


# Insert user into database
def insert_user(usr):
    c = database_connection()
    response = ''

    # New user ==> Insert
    try:
        c.execute('''INSERT INTO users(reg_date, email, firstname, lastname, age, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, savings_limit, savings_limit_bank, retirement, retirement_bank, usagesalary, usagesalary_bank) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                 (usr.reg_date, usr.email, usr.firstname, usr.lastname, usr.age, usr.postal_number, usr.street_name, usr.street_number, usr.phone, usr.bsu, usr.bsu_bank, usr.savings, usr.savings_bank, usr.savings_limit, usr.savings_limit_bank, usr.retirement, usr.retirement_bank, usr.usagesalary, usr.usagesalary_bank))
        response = 'new_user'

    # User exist ==> Update
    except sqlite3.IntegrityError:
        c.execute('''UPDATE users SET firstname = ?, lastname = ?, age = ?, postal_number = ?, street_name = ?, street_number = ?, phone = ?, bsu = ?, bsu_bank = ?, savings = ?, savings_bank = ?, savings_limit = ?, savings_limit_bank = ?, retirement = ?, retirement_bank = ?, usagesalary = ?, usagesalary_bank = ? WHERE email = ?''',
                 (usr.firstname, usr.lastname, usr.age, usr.postal_number, usr.street_name, usr.street_number, usr.phone, usr.bsu, usr.bsu_bank, usr.savings, usr.savings_bank, usr.savings_limit, usr.savings_limit_bank, usr.retirement, usr.retirement_bank, usr.usagesalary, usr.usagesalary_bank, usr.email))
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

# Database lookup for savings banks
def savings_look(usr, account_type):
    if account_type == 'bsu':
        bank_name = (usr.bsu_bank).split(' [')[0]
        bank_account_name = (usr.bsu_bank).split('[')[1].replace('[', '').replace(']', '')
    elif account_type == 'savings_nolimit':
        bank_name = (usr.savings_bank).split(' [')[0]
        bank_account_name = (usr.savings_bank).split('[')[1].replace('[', '').replace(']', '')
    elif account_type == 'savings_limit':
        bank_name = (usr.savings_limit_bank).split(' [')[0]
        bank_account_name = (usr.savings_limit_bank).split('[')[1].replace('[', '').replace(']', '')
    elif account_type == 'retirement':
        bank_name = (usr.retirement_bank).split(' [')[0]
        bank_account_name = (usr.retirement_bank).split('[')[1].replace('[', '').replace(']', '')
    elif account_type == 'usage_salary':
        bank_name = (usr.usagesalary_bank).split(' [')[0]
        bank_account_name = (usr.usagesalary_bank).split('[')[1].replace('[', '').replace(']', '')
    else:
        bank_name = ''
        bank_account_name = ''

    return bank_name, bank_account_name


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
        retirement          = row[16]
        retirement_bank     = row[17]
        usagesalary         = row[18]
        usagesalary_bank    = row[19]

        current_user = User(reg_date, email, firstname, lastname, age, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, savings_limit, savings_limit_bank, retirement, retirement_bank, usagesalary, usagesalary_bank)
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


# Get savings banks
def get_saving_banks(account_type):
    c = database_connection()

    savings_banks = []

    sql_cmd_s = c.execute('''SELECT bank_name, bank_account_name FROM saving WHERE account_type = ? ORDER BY bank_name ASC''', (account_type,))

    for row in sql_cmd_s:
        bank_account = row[0] + ' [' + row[1] + ']'
        savings_banks.append(bank_account)

    c.close()

    return savings_banks


# Get specific savings banks with higher interest rates
def get_saving_banks_with_higher_rates(usr, account_type):
    c = database_connection()
    
    lookup = savings_look(usr, account_type)
    bank_name = lookup[0]
    bank_account_name = lookup[1]

    sql_cmd_interest = c.execute('''SELECT interest_rate FROM saving WHERE account_type = ? AND bank_name = ? AND bank_account_name = ?''', (account_type, bank_name, bank_account_name))
    
    current_rate = 0
    for row in sql_cmd_interest:
        current_rate = row[0]

    # Select the banks with higher rates
    if account_type == 'savings_limit':
        user_age = usr.age
        if int(user_age) > 34:
            sql_cmd_s = c.execute('''SELECT * FROM saving WHERE limit_age = 0 AND account_type = ? AND interest_rate > ? ''', (account_type, current_rate))
        else:
            sql_cmd_s = c.execute('''SELECT * FROM saving WHERE account_type = ? AND interest_rate > ? ''', (account_type, current_rate))
    else:
        sql_cmd_s = c.execute('''SELECT * FROM saving WHERE account_type = ? AND interest_rate > ?''', (account_type, current_rate))

    results = []
    for row in sql_cmd_s:
        account_type      = row[0]
        product_id        = row[1]
        bank_id           = row[2]
        bank_name         = row[3]
        bank_url          = row[4]
        bank_region       = row[5]
        bank_account_name = row[6]
        publication_date  = row[7]
        interest_rate     = row[8]
        limit_age         = row[9]

        current_saving_bank = Saving(account_type, product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age)
        results.append(current_saving_bank)

    c.close()

    # Sort the results based on interest rate
    results = sorted(results, key=lambda x: x.interest_rate, reverse=True)

    return results


# Get user's specific savings bank id
def get_user_savings_bank_id(usr, account_type):
    c = database_connection()

    lookup = savings_look(usr, account_type)
    bank_name = lookup[0]
    bank_account_name = lookup[1]

    sql_cmd_s = c.execute('''SELECT bank_id FROM saving WHERE account_type = ? AND bank_name = ? AND bank_account_name = ?''', (account_type, bank_name, bank_account_name))

    id = ''
    for row in sql_cmd_s:
        id = row[0]

    c.close()

    return id
