import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from db import get_user_savings_bank_id
from settings import url_change_bank, credentials, time_now


# New user registration confirmation email
def registration_email(usr):
    TO = usr.email
    FROM = credentials()[0]
    SUBJECT = 'Velkommen til Finansvarsel!'

    reg_firstname = usr.firstname
    reg_lastname = usr.lastname

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei """ + reg_firstname + """ """ + reg_lastname + """,<br></p>
      <p>Velkommen som ny bruker på Finansvarsel! Du vil motta nyhetsmail om banker fra oss en gang i uken.</p>
      <p>Alle våre data er hentet fra <a href='https://www.finansportalen.no'>Finansportalen</a>.<br></p>
      <p>Med vennlig hilsen,<br>
      Finansvarsel<br>
      http://fredrikbakken.no</p>
    </body>
    """

    send_email(SUBJECT, email_content, TO, FROM)


# Update user data confirmation email
def update_email(usr):
    TO = usr.email
    FROM = credentials()[0]
    SUBJECT = 'Finansvarsel - Brukeroppdatering'

    upd_firstname           = usr.firstname
    upd_lastname            = usr.lastname
    upd_age                 = usr.age
    upd_postal_number       = usr.postal_number
    upd_street_name         = usr.street_name
    upd_street_number       = usr.street_number
    upd_phone               = usr.phone
    upd_bsu                 = usr.bsu
    upd_bsu_bank            = usr.bsu_bank
    upd_savings             = usr.savings
    upd_savings_bank        = usr.savings_bank
    upd_savings_limit       = usr.savings_limit_bank
    upd_savings_limit_bank  = usr.savings_limit_bank
    upd_retirement          = usr.retirement
    upd_retirement_bank     = usr.retirement_bank
    upd_usagesalary         = usr.usagesalary
    upd_usagesalary_bank    = usr.usagesalary_bank

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei """ + upd_firstname + """ """ + upd_lastname + """,<br></p>
      <p>Vi har registrert din brukeroppdatering på Finansvarsel og har lagret følgende om deg:<br>
      Fornavn: """ + upd_firstname + """<br>
      Etternavn: """ + upd_lastname + """<br>
      Alder: """ + upd_age + """<br>
      Postnummer: """ + upd_postal_number + """<br>
      Gatenavn: """ + upd_street_name + """<br>
      Gatenummer: """ + upd_street_number + """<br>
      Telefon/Mobil: """ + upd_phone + """<br>
      Er du interessert i BSU-konto? """ + upd_bsu + """<br>
      BSU bank: """ + upd_bsu_bank + """<br>
      Er du interessert i sparekonto (uten bruksbegrensning)? """ + upd_savings + """<br>
      Sparekonto bank (uten bruksbegrensning): """ + upd_savings_bank + """<br>
      Er du interessert i sparekonto (med bruksbegrensning)? """ + upd_savings_limit + """<br>
      Sparekonto bank (med bruksbegrensning): """ + upd_savings_limit_bank + """<br>
      Er du interessert i pensjonssparekonto? """ + upd_retirement + """<br>
      Pensjonssparekonto bank: """ + upd_retirement_bank + """<br>
      Er du interessert i bruks-/lønnskonto? """ + upd_usagesalary + """<br>
      Bruks-/lønnskonto bank: """ + upd_usagesalary_bank + """</p>
      <p>Alle våre data er hentet fra <a href='https://www.finansportalen.no'>Finansportalen</a>.<br></p>
      <p>Med vennlig hilsen,<br>
      Finansvarsel<br>
      http://fredrikbakken.no</p>
    </body>
    """

    send_email(SUBJECT, email_content, TO, FROM)


# Delete user data confirmation email
def delete_email(email, store):
    TO = email
    FROM = credentials()[0]
    SUBJECT = 'Finansvarsel - Slett min bruker'

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei,<br></p>
      <p>Vi i Finansvarsel har mottat ditt ønske om å slette dine brukeropplysninger fra våre registre og ikke lengre motta ukentlige eposter fra oss.</p>"""

    if store == "Ja":
        email_content += """<p>Etter deres ønsker har vi lagret din epost, """ + email + """, for å sende deg varseler om større oppdateringer i våre systemer.</p>"""

    email_content += """
      <p>Takk for at du har testet Finansvarsel og vi ønsker deg velkommen igjen ved en senere anledning!</p>
      <p>Alle våre data er hentet fra <a href='https://www.finansportalen.no'>Finansportalen</a>.<br></p>
      <p>Med vennlig hilsen,<br>
      Finansvarsel<br>
      http://fredrikbakken.no</p>
    </body>
    """

    send_email(SUBJECT, email_content, TO, FROM)


def news_email(usr, saving_data): #bsu_data, savings_account_data, savings_limit_account_data, retirement_data, usagesalary_data):
    TO = usr.email
    FROM = credentials()[0]
    SUBJECT = 'Oppdatering fra Finansvarsel: ' + time_now('date.month.year')

    news_firstname = usr.firstname
    news_lastname = usr.lastname

    bsu_data = saving_data[0]
    savings_account_data = saving_data[1]
    savings_limit_account_data = saving_data[2]
    retirement_data = saving_data[3]
    usagesalary_data = saving_data[4]

    number_of_bsu_banks = str(len(bsu_data))
    number_of_savings_banks = str(len(savings_account_data))
    number_of_savings_limit_banks = str(len(savings_limit_account_data))
    number_of_retirement_banks = str(len(retirement_data))
    number_of_usagesalary_banks = str(len(usagesalary_data))

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei """ + news_firstname + """ """ + news_lastname + """,<br></p>
      <p><br></p>
      <p>
    """

    ## Adding BSU data
    if not bsu_data == '':
        email_content += """
          <b>Boligsparing Ungdom (BSU):</b> Finansvarsel har registrert <b>""" + number_of_bsu_banks + """</b> kontoer i norske banker med bedre rentevilkår enn banken du i dag vurderer/benytter:<p>
        """

        yourBankId = get_user_savings_bank_id(usr, 'bsu')
        productType = 'banksparing'
        product = 'bsu'
        for x in range(len(bsu_data)):
            seletectedBankId = bsu_data[x].bank_id
            url_change_bsu_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = bsu_data[x].bank_name

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % bsu_data[x].interest_rate + """%. <a href='""" + bsu_data[x].bank_url + """'>""" + bank_name + """</a>. Søk om å bytte til """ + bank_name + """: """ + url_change_bsu_bank + """</p>
            """

        email_content += """<p><br></p>"""

    ## Adding savings account data
    if not savings_account_data == '':
        email_content += """
          <b>Sparekonto / Innskuddskonto (uten bruksbegrensning):</b> Finansvarsel har registrert <b>""" + number_of_savings_banks + """</b> kontoer i norske banker med bedre rentevilkår enn banken du i dag vurderer/benytter:<br>
        """

        yourBankId = get_user_savings_bank_id(usr, 'savings_nolimit')
        productType = 'banksparing'
        product = 'bankinnskudd'
        for x in range(len(savings_account_data)):
            seletectedBankId = savings_account_data[x].bank_id
            url_change_savings_nolimit_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = savings_account_data[x].bank_name

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % savings_account_data[x].interest_rate + """%. <a href='""" + savings_account_data[x].bank_url + """'>""" + bank_name + """</a>. Søk om å bytte til """ + bank_name + """: """ + url_change_savings_nolimit_bank + """</p>
            """
        
        email_content += """<p><br></p>"""

    ## Adding savings limit account data
    if not savings_limit_account_data == '':
        email_content += """
          <b>Sparekonto / Innskuddskonto (med bruksbegrensning):</b> Finansvarsel har registrert <b>""" + number_of_savings_limit_banks + """</b> kontoer i norske banker med bedre rentevilkår enn banken du i dag vurderer/benytter:<br>
        """

        yourBankId = get_user_savings_bank_id(usr, 'savings_limit')
        productType = 'banksparing'
        product = 'bankinnskudd'
        for x in range(len(savings_limit_account_data)):
            seletectedBankId = savings_limit_account_data[x].bank_id
            url_change_savings_limit_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = savings_limit_account_data[x].bank_name

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % savings_limit_account_data[x].interest_rate + """%. <a href='""" + savings_limit_account_data[x].bank_url + """'>""" + bank_name + """</a>. Søk om å bytte til """ + bank_name + """: """ + url_change_savings_limit_bank + """</p>
            """

        email_content += """<p><br></p>"""
    
    ## Adding retirement account data
    if not retirement_data == '':
        email_content += """
          <b>Pensjonssparekonto:</b> Finansvarsel har registrert <b>""" + number_of_retirement_banks + """</b> kontoer i norske banker med bedre rentevilkår enn banken du i dag vurderer/benytter:<br>
        """

        yourBankId = get_user_savings_bank_id(usr, 'retirement')
        productType = 'banksparing'
        product = 'bankinnskudd'
        for x in range(len(retirement_data)):
            seletectedBankId = retirement_data[x].bank_id
            url_change_retirement_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = retirement_data[x].bank_name

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % retirement_data[x].interest_rate + """%. <a href='""" + retirement_data[x].bank_url + """'>""" + bank_name + """</a>. Søk om å bytte til """ + bank_name + """: """ + url_change_retirement_bank + """</p>
            """

        email_content += """<p><br></p>"""

    ## Adding usage / salary data
    if not usagesalary_data == '':
        email_content += """
          <b>Bruks-/lønnskonto:</b> Finansvarsel har registrert <b>""" + number_of_usagesalary_banks + """</b> kontoer i norske banker med bedre rentevilkår enn banken du i dag vurderer/benytter:<br>
        """

        yourBankId = get_user_savings_bank_id(usr, 'usage_salary')
        productType = 'banksparing'
        product = 'bankinnskudd'
        for x in range(len(usagesalary_data)):
            seletectedBankId = usagesalary_data[x].bank_id
            url_change_usagesalary_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = (usagesalary_data[x].bank_name)

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % usagesalary_data[x].interest_rate + """%. <a href='""" + usagesalary_data[x].bank_url + """'>""" + bank_name + """</a>. Søk om å bytte til """ + bank_name + """: """ + url_change_usagesalary_bank + """</p>
            """

        email_content += """<p><br></p>"""

    email_content += """
      <p>Tusen takk for at du benytter Finansvarsel som er utviklet av Fredrik Bakken. Prosjektet hadde ikke vært mulig uten dataene <a href='https://www.finansportalen.no'>Finansportalen</a> tilbyr.<br></p>
      <p>Med vennlig hilsen,<br>
      Finansvarsel<br>
      http://fredrikbakken.no</p>
    """

    send_email(SUBJECT, email_content, TO, FROM)


def send_email(SUBJECT, BODY, TO, FROM):
    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)

    # The actual sending of the e-mail
    server = smtplib.SMTP(credentials()[2])
    server.ehlo()
    server.starttls()
    server.login(credentials()[0], credentials()[1])
    server.sendmail(FROM, TO, MESSAGE.as_string())
    server.quit()

    print('Email to ' + TO + ' has been sent.')
