
from db import insert_user
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
        name = new_user[1]
        email = new_user[2]
        age = new_user[3]
        bsu = new_user[4]
        bsu_bank = new_user[5]

        # Insert new user into the user database
        insert_user(name, email, age, bsu, bsu_bank)

    # Loop through and delete user entries in sheet
    print('Deleting new user entries from sheet...')
    for x in range(number_of_users):
        users_sheet.delete_row((number_of_users + 1) - x)
