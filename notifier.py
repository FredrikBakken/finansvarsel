
from db import get_bsu_banks_with_higher_rates, get_savings_account_banks_with_higher_rates, get_savings_account_limit_banks_with_higher_rates


# Method for printing notification data
def print_notification_results(usr, results):
    print('\n' + usr.firstname + ' ' + usr.lastname)
    for y in range(len(results)):
        try:
            print(results[y])
        except:
            print('Issues while trying to print results.')


# Getting BSU banks with higher rates
def bsu_notifier(usr):
    if not usr.bsu == 'Nei':
        results = get_bsu_banks_with_higher_rates(usr)
    else:
        results = ''
        print('Ingen interesse for BSU-konto registrert.')

    print_notification_results(usr, results)

    return results


# Getting savings banks with higher rates
def savings_account_notifier(usr):
    if not usr.savings == 'Nei':
        results = get_savings_account_banks_with_higher_rates(usr)
    else:
        results = ''
        print('Ingen interesse for sparekonto registrert.')

    print_notification_results(usr, results)

    return results


# Getting savings limit banks with higher rates
def savings_limit_account_notifier(usr):
    if not usr.savings_limit == 'Nei':
        results = get_savings_account_limit_banks_with_higher_rates(usr)
    else:
        results = ''
        print('Ingen interesse for sparekonto med bruksbegrensing registrert.')

    results = sorted(results, key=lambda x:x[7], reverse=True)

    print_notification_results(usr, results)

    return results
