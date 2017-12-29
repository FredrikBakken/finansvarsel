
from db import get_bsu_banks_with_higher_rates, get_savings_account_banks_with_higher_rates


# Method for printing notification data
def print_notification_results(user, results):
    print('\n' + user[2] + ' ' + user[3])
    for y in range(len(results)):
        try:
            print(results[y])
        except:
            print('Issues while trying to print results.')


# Getting BSU banks with higher rates
def bsu_notifier(user):
    if not user[8] == 'Nei':
        results = get_bsu_banks_with_higher_rates(user)
    else:
        results = ''
        print('Ingen interesse for BSU-konto registrert.')

    print_notification_results(user, results)

    return results


# Getting savings banks with higher rates
def savings_account_notifier(user):
    if not user[10] == 'Nei':
        results = get_savings_account_banks_with_higher_rates(user)
    else:
        results = ''
        print('Ingen interesse for sparekonto registrert.')

    print_notification_results(user, results)

    return results
