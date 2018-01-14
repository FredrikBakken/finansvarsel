
## USER CLASS (handles user specific data)
class User:
    def __init__(self, reg_date, email, firstname, lastname, age, postal_number, street_name, street_number, phone, bsu, bsu_bank, savings, savings_bank, savings_limit, savings_limit_bank, retirement, retirement_bank, usagesalary, usagesalary_bank):
        self.reg_date = reg_date
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.postal_number = postal_number
        self.street_name = street_name
        self.street_number = street_number
        self.phone = phone
        self.bsu = bsu
        self.bsu_bank = bsu_bank
        self.savings = savings
        self.savings_bank = savings_bank
        self.savings_limit = savings_limit
        self.savings_limit_bank = savings_limit_bank
        self.retirement = retirement
        self.retirement_bank = retirement_bank
        self.usagesalary = usagesalary
        self.usagesalary_bank = usagesalary_bank


## SAVING CLASS (handles savings account specific data)
class Saving:
    def __init__(self, account_type, product_id, bank_id, bank_name, bank_url, bank_region, bank_account_name, publication_date, interest_rate, limit_age):
        self.account_type = account_type
        self.product_id = product_id
        self.bank_id = bank_id
        self.bank_name = bank_name
        self.bank_url = bank_url
        self.bank_region = bank_region
        self.bank_account_name = bank_account_name
        self.publication_date = publication_date
        self.interest_rate = interest_rate
        self.limit_age = limit_age


## LOAN CLASS (TODO for the future)
