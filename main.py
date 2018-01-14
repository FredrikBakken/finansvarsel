import sys
import scheduler

from db import get_all_users, get_specific_user
from data import get_bsu_data, get_savings_acc_nolimit_data, get_savings_acc_limit_data, get_retirement_data, get_usage_and_salary_data
from user import register_users, remove_users
from emailer import news_email
from notifier import bsu_notifier, savings_account_notifier, savings_limit_account_notifier, retirement_notifier, usagesalary_notifier
#from settings import db_decryption, db_encryption


# FINANCE CONTROLLER
# About the Finance Controller:
# 1. Downloading data from finansportalen.no
# 2. Stores fetched data into the database
# 3. Updates the form based on collected data
def finance_controller():
    ## Collect and store BSU data
    get_bsu_data()

    ## Collect and store savings account data (no limit)
    get_savings_acc_nolimit_data()

    ## Collect and store savings account data (limitations)
    get_savings_acc_limit_data()

    ## Collect and store retirement data
    get_retirement_data()

    ## Collect and store usage and salary data
    get_usage_and_salary_data()


# USER CONTROLLER
# About the User Controller:
# 1. Fetches user updates (new registration, updates, and deletes)
# 2. Stores and removes user data from the database
# 3. Connects the user table data with finance tables
def user_controller():
    ## Register new/updated user entries
    register_users()

    ## Delete user entries
    remove_users()


# NOTIFICATION CONTROLLER
def notification_controller():
    # Get all users
    users = get_all_users()
    
    for x in range(len(users)):
        bsu_data = bsu_notifier(users[x])
        savings_account_data = savings_account_notifier(users[x])
        savings_limit_account_data = savings_limit_account_notifier(users[x])
        retirement_data = retirement_notifier(users[x])
        usagesalary_data = usagesalary_notifier(users[x])

        # Send finance data by email to specific user
        news_email(users[x], bsu_data, savings_account_data, savings_limit_account_data, retirement_data, usagesalary_data)


def run():
    #finance_controller()
    #user_controller()
    notification_controller()

    #get_savings_acc_limit_data()

    #register_users()
    #users = get_all_users()
    #print(db_decryption(users[0][1]).decode())

    #value = get_specific_user(db_encryption('username'.encode()))
    #print(value)
    #print(db_decryption(value[0][1]).decode())


if __name__ == "__main__":
    argument = sys.argv
    try:
        if argument[1] == 'auto':
            scheduler.thread_scheduler()
    except:
        run()
