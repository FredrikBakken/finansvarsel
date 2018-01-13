
from db import create_user_table, inactive_user_table, insert_user, delete_user
from classes import User
from emailer import registration_email, update_email, delete_email
from settings import access_spreadsheet, time_now


### USER CONTROLLER

# Register new users and user updates
def register_users():
    ## SQLite3 user database initialization
    create_user_table()

    # Open users worksheet
    sheet = access_spreadsheet()
    users_sheet = sheet.get_worksheet(0)

    # Get number of rows (new user registrations)
    number_of_users = (users_sheet.row_count - 1)
    print('Number of new registrations: ' + str(number_of_users))

    # Loop through new user registrations
    for x in range(number_of_users):
        new_user = users_sheet.row_values(2 + x)
        #print('New user ' + str(x + 1) + ': ' + str(new_user))

        # Formatting user data
        reg_date = time_now('date.month.year')
        email = new_user[1]
        firstname = new_user[2]
        lastname = new_user[3]
        age = new_user[4]
        postal_number = new_user[5]
        street_name = new_user[6]
        street_number = new_user[7]
        phone = new_user[8]
        bsu = new_user[9]
        bsu_bank = new_user[10]
        savings = new_user[11]
        savings_bank = new_user[12]
        savings_limit = new_user[13]
        savings_limit_bank = new_user[14]

        # Formatting current user to class
        current_user = User(reg_date, email, firstname, lastname, age, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, savings_limit, savings_limit_bank)
        
        # Insert new user into the user database
        response = insert_user(current_user)
        
        # Send confirmation email for new registrations and updates
        if response == 'new_user':
            registration_email(current_user)
        elif response == 'update_user':
            update_email(current_user)
            
    # Loop through and delete user entries in sheet
    print('Deleting new user entries from sheet...')
    for x in range(number_of_users):
        users_sheet.delete_row((number_of_users + 1) - x)

# Delete user
def remove_users():
    ## SQLite3 inactive_user database initialization
    inactive_user_table()

    # Open delete users worksheet
    sheet = access_spreadsheet()
    remove_sheet = sheet.get_worksheet(1)

    # Get number of rows (new user registrations)
    number_of_users = (remove_sheet.row_count - 1)
    print('Number of user(s) to remove: ' + str(number_of_users))

    # Loop through new user registrations
    for x in range(number_of_users):
        remove_user = remove_sheet.row_values(2 + x)
        print('Delete user ' + str(x + 1) + ': ' + str(remove_user))

        # Formatting user data
        email = remove_user[1]
        reason = remove_user[2]
        store = remove_user[3].split(',', 1)[0]

        # Delete user from user database
        delete_user(email, reason, store)

        # Send confirmation email for deleted user
        delete_email(email, store)

    # Loop through and delete user entries in sheet
    print('Deleting delete user entries from sheet...')
    for x in range(number_of_users):
        remove_sheet.delete_row((number_of_users + 1) - x)
