
from db import get_user_current_bsu_bank, get_banks_with_higher_rates

def bsu_notifier():
    # Get all users
    user = get_user_current_bsu_bank()

    for x in range(len(user)):
        print('\n' + user[x][1])
        results = get_banks_with_higher_rates(user[x])

        for y in range(len(results)):
            print(results[y])