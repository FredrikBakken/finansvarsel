
from db import create_user_table, get_user_current_bsu_bank
from data import get_bsu_data, get_savings_data
from user import register_users
from notifier import bsu_notifier


# FINANCE CONTROLLER
# About the Finance Controller:
# 1. Downloading data from finansportalen.no
# 2. Stores fetched data into the database
# 3. Updates the form based on collected data
def finance_controller():
    ## Collect and store BSU data
    get_bsu_data()

    ## Collect and store savings data
    get_savings_data()

    ## etc.


# USER CONTROLLER
# About the User Controller:
# 1. Fetches user updates (new registration, updates, and deletes)
# 2. Stores user data into the database
# 3. Connects the user table data with finance tables
def user_controller():
    ## SQLite3 database initialization
    create_user_table()

    ## Register new user entries
    register_users()

    ## Get all users and connected BSU banks
    data = get_user_current_bsu_bank()
    for x in range(len(data)):
        print(data[x])


# NOTIFICATION CONTROLLER
def notification_controller():
    bsu_notifier()



def run():
    #finance_controller()
    user_controller()
    notification_controller()


if __name__ == "__main__":
    run()
