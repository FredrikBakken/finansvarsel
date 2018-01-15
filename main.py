import sys
import scheduler

from db import get_all_users
from data import get_savings_data
from user import register_users, remove_users
from emailer import news_email
from notifier import savings_notifier

account_types = [['bsu', 2], ['savings_nolimit', 3], ['savings_limit', 4], ['retirement', 5], ['usage_salary', 6]]

# FINANCE CONTROLLER
# About the Finance Controller:
# 1. Downloading data from finansportalen.no
# 2. Stores fetched data into the database
# 3. Updates the form based on collected data
def finance_controller():
    ## Collect and store savings data
    get_savings_data(account_types)


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
        # Get all saving bank data
        saving_data = savings_notifier(users[x], account_types)

        # Send finance data by email to specific user
        news_email(users[x], saving_data)


def run():
    finance_controller()
    user_controller()
    notification_controller()


if __name__ == "__main__":
    argument = sys.argv
    try:
        if argument[1] == 'auto':
            scheduler.thread_scheduler()
    except:
        run()
