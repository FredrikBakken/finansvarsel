
from db import get_saving_banks_with_higher_rates


# Method for printing notification data
def print_notification_results(usr, results):
    print('\n' + usr.firstname + ' ' + usr.lastname)
    for y in range(len(results)):
        try:
            local_interest_rate     = float(results[y].interest_rate)
            local_bank_name         = str(results[y].bank_name)
            local_bank_account_name = str(results[y].bank_account_name)
            print('%.2f' % local_interest_rate + '%   ' + local_bank_name + '  [' + local_bank_account_name + ']')
        except:
            print('Issues while trying to print results.')


# Get specific savings banks with higher rates
def savings_notifier(usr, account_type):
    # BSU Banks
    if not usr.bsu == 'Nei' and account_type[0][0] == 'bsu':
        bsu_results = get_saving_banks_with_higher_rates(usr, account_type[0][0])
        print_notification_results(usr, bsu_results)
    else:
        bsu_results = ''
    
    # Savings no limit Banks
    if not usr.savings == 'Nei' and account_type[1][0] == 'savings_nolimit':
        savings_nolimit_results = get_saving_banks_with_higher_rates(usr, account_type[1][0])
        print_notification_results(usr, savings_nolimit_results)
    else:
        savings_nolimit_results = ''
    
    # Savings limit Banks
    if not usr.savings_limit == 'Nei' and account_type[2][0] == 'savings_limit':
        savings_limit_results = get_saving_banks_with_higher_rates(usr, account_type[2][0])
        print_notification_results(usr, savings_limit_results)
    else:
        savings_limit_results = ''
    
    # Retirement Banks
    if not usr.retirement == 'Nei' and account_type[3][0] == 'retirement':
        retirement_results = get_saving_banks_with_higher_rates(usr, account_type[3][0])
        print_notification_results(usr, retirement_results)
    else:
        retirement_results = ''

    # Usage and salary Banks
    if not usr.usagesalary == 'Nei' and account_type[4][0] == 'usage_salary':
        usagesalary_results = get_saving_banks_with_higher_rates(usr, account_type[4][0])
        print_notification_results(usr, usagesalary_results)
    else:
        usagesalary_results = ''
    
    return bsu_results, savings_nolimit_results, savings_limit_results, retirement_results, usagesalary_results
