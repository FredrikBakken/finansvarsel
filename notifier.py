
from db import get_banks_with_higher_rates
from settings import url_change_bank

def bsu_notifier(user):
    print('\n' + user[0] + ' ' + user[1])
    results = get_banks_with_higher_rates(user)

    for y in range(len(results)):
        print(results[y])

    return results
