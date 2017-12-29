
from db import get_users_current_bsu_bank
from data import get_bsu_data
from user import register_users, remove_users
from emailer import news_email
from notifier import bsu_notifier


# FINANCE CONTROLLER
# About the Finance Controller:
# 1. Downloading data from finansportalen.no
# 2. Stores fetched data into the database
# 3. Updates the form based on collected data
def finance_controller():
    ## Collect and store BSU data
    get_bsu_data()


# USER CONTROLLER
# About the User Controller:
# 1. Fetches user updates (new registration, updates, and deletes)
# 2. Stores and removes user data from the database
# 3. Connects the user table data with finance tables
def user_controller():
    ## Register new user entries
    register_users()

    ## Delete user entries
    remove_users()


# NOTIFICATION CONTROLLER
def notification_controller():
    # Get all users
    users = get_users_current_bsu_bank()

    for x in range(len(users)):
        bsu_data = bsu_notifier(users[x])

        # ALL OTHER DATA

        # SEND EMAIL TO CURRENT USER
        #news_email(users[x], bsu_data)


def run():
    finance_controller()
    user_controller()
    notification_controller()

if __name__ == "__main__":
    run()
