
from db import get_bsu_banks_with_higher_rates, get_savings_account_banks_with_higher_rates

def bsu_notifier(user):
    print('\n' + user[2] + ' ' + user[3])

    if not user[8] == 'Nei':
        results = get_bsu_banks_with_higher_rates(user)
    else:
        results = ''

    for y in range(len(results)):
        print(results[y])

    return results

def savings_account_notifier(user):
    print('\n' + user[2] + ' ' + user[3])

    if not user[10] == 'Nei':
        results = get_savings_account_banks_with_higher_rates(user)
    else:
        results = ''

    for y in range(len(results)):
        print(results[y])

    return results
