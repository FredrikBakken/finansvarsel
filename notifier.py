
from db import get_saving_banks_with_higher_rates


# Method for printing notification data
def print_notification_results(usr, results, account_type):
    print('\n' + usr.firstname + ' ' + usr.lastname + '  [ ' + account_type + ' ]')
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
    if not usr.bsu == 'Nei':
        bsu_results = get_saving_banks_with_higher_rates(usr, account_type[0][0])
        print_notification_results(usr, bsu_results, account_type[0][0])                        # Used for testing db output
    else:
        bsu_results = ''
    
    # Savings no limit Banks
    if not usr.savings == 'Nei':
        savings_nolimit_results = get_saving_banks_with_higher_rates(usr, account_type[1][0])
        print_notification_results(usr, savings_nolimit_results, account_type[1][0])            # Used for testing db output
    else:
        savings_nolimit_results = ''
    
    # Savings limit Banks
    if not usr.savings_limit == 'Nei':
        savings_limit_results = get_saving_banks_with_higher_rates(usr, account_type[2][0])
        print_notification_results(usr, savings_limit_results, account_type[2][0])              # Used for testing db output
    else:
        savings_limit_results = ''
    
    # Retirement Banks
    if not usr.retirement == 'Nei':
        retirement_results = get_saving_banks_with_higher_rates(usr, account_type[3][0])
        print_notification_results(usr, retirement_results, account_type[3][0])                 # Used for testing db output
    else:
        retirement_results = ''

    # Usage and salary Banks
    if not usr.usagesalary == 'Nei':
        usagesalary_results = get_saving_banks_with_higher_rates(usr, account_type[4][0])
        print_notification_results(usr, usagesalary_results, account_type[4][0])                # Used for testing db output
    else:
        usagesalary_results = ''
    
    return bsu_results, savings_nolimit_results, savings_limit_results, retirement_results, usagesalary_results
