
from db import insert_user, get_users_current_bsu_bank
from settings import access_spreadsheet

### USER CONTROLLER

# Register new users and user updates
def register_users():
    # Open users worksheet
    sheet = access_spreadsheet()
    users_sheet = sheet.get_worksheet(0)

    # Get number of rows (new user registrations)
    number_of_users = (users_sheet.row_count - 1)
    print('Number of new registrations: ' + str(number_of_users))

    # Loop through new user registrations
    for x in range(number_of_users):
        new_user = users_sheet.row_values(2 + x)
        print('New user ' + str(x + 1) + ': ' + str(new_user))

        # Formatting user data
        email = new_user[1]
        firstname = new_user[2]
        lastname = new_user[3]
        postal_number = new_user[4]
        street_name = new_user[5]
        street_number = new_user[6]
        phone = new_user[7]
        bsu = new_user[8]
        bsu_bank = new_user[9]

        # Insert new user into the user database
        insert_user(email, firstname, lastname, postal_number, street_name, street_number, phone, bsu, bsu_bank)

    # Loop through and delete user entries in sheet
    print('Deleting new user entries from sheet...')
    for x in range(number_of_users):
        users_sheet.delete_row((number_of_users + 1) - x)

    ## Get all users and connected BSU banks
    data = get_users_current_bsu_bank()
    for x in range(len(data)):
        print(data[x])
