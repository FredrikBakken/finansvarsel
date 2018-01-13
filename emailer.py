import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from db import get_user_bsu_bank_id, get_user_savings_bank_id
from settings import url_change_bank, credentials, email_strings, time_now


# New user registration confirmation email
def registration_email(usr):
    TO = usr.email
    FROM = credentials()[0]
    SUBJECT = email_strings('Velkommen til Finansvarsel!')

    reg_firstname = email_strings(usr.firstname)
    reg_lastname = email_strings(usr.lastname)

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei """ + reg_firstname + """ """ + reg_lastname + """,<br></p>
      <p>Velkommen som ny bruker pÃ¥ Finansvarsel! Du vil motta nyhetsmail om banker fra oss en gang i uken.</p>
      <p>Alle vÃ¥re data er hentet fra <a href='https://www.finansportalen.no'>Finansportalen</a>.<br></p>
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
    SUBJECT = email_strings('Finansvarsel - Brukeroppdatering')

    upd_firstname     = email_strings(usr.firstname)
    upd_lastname      = email_strings(usr.lastname)
    upd_age           = email_strings(usr.age)
    upd_postal_number = email_strings(usr.postal_number)
    upd_street_name   = email_strings(usr.street_name)
    upd_street_number = email_strings(usr.street_number)
    upd_phone         = email_strings(usr.phone)
    upd_bsu           = email_strings(usr.bsu)
    upd_bsu_bank      = email_strings(usr.bsu_bank)
    upd_savings       = email_strings(usr.savings)
    upd_savings_bank  = email_strings(usr.savings_bank)

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei """ + upd_firstname + """ """ + upd_lastname + """,<br></p>
      <p>Vi har registrert din brukeroppdatering pÃ¥ Finansvarsel og har lagret fÃ¸lgende om deg:<br>
      Fornavn: """ + upd_firstname + """<br>
      Etternavn: """ + upd_lastname + """<br>
      Alder: """ + upd_age + """<br>
      Postnummer: """ + upd_postal_number + """<br>
      Gatenavn: """ + upd_street_name + """<br>
      Gatenummer: """ + upd_street_number + """<br>
      Telefon/Mobil: """ + upd_phone + """<br>
      Er du interessert i BSU-konto? """ + upd_bsu + """<br>
      BSU bank: """ + upd_bsu_bank + """<br>
      Er du interessert i sparekonto? """ + upd_savings + """<br>
      Sparekonto bank: """ + upd_savings_bank + """</p>
      <p>Alle vÃ¥re data er hentet fra <a href='https://www.finansportalen.no'>Finansportalen</a>.<br></p>
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
    SUBJECT = email_strings('Finansvarsel - Slett min bruker')

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei,<br></p>
      <p>Vi i Finansvarsel har mottat ditt Ã¸nske om Ã¥ slette dine brukeropplysninger fra vÃ¥re registre og ikke lengre motta ukentlige eposter fra oss.</p>"""

    if store == "Ja":
        email_content += """<p>Etter deres Ã¸nsker har vi lagret din epost, """ + email + """, for Ã¥ sende deg varseler om stÃ¸rre oppdateringer i vÃ¥re systemer.</p>"""

    email_content += """
      <p>Takk for at du har testet Finansvarsel og vi Ã¸nsker deg velkommen igjen ved en senere anledning!</p>
      <p>Alle vÃ¥re data er hentet fra <a href='https://www.finansportalen.no'>Finansportalen</a>.<br></p>
      <p>Med vennlig hilsen,<br>
      Finansvarsel<br>
      http://fredrikbakken.no</p>
    </body>
    """

    send_email(SUBJECT, email_content, TO, FROM)


def news_email(usr, bsu_data, savings_account_data):
    TO = usr.email
    FROM = credentials()[0]
    SUBJECT = email_strings('Oppdatering fra Finansvarsel: ' + time_now('date.month.year'))

    news_firstname = email_strings(usr.firstname)
    news_lastname = email_strings(usr.lastname)

    number_of_bsu_banks = str(len(bsu_data))
    number_of_savings_banks = str(len(savings_account_data))

    email_content = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>""" + SUBJECT + """</title>
    </head>
    <body>
      <p>Hei """ + news_firstname + """ """ + news_lastname + """,<br></p>
      <p>
    """

    ## Adding BSU-data
    if not bsu_data == '':
        email_content += """
          <b>Boligsparing Ungdom (BSU):</b> Finansvarsel har registrert """ + number_of_bsu_banks + """ kontoer i norske banker med bedre rentevilkÃ¥r enn banken du i dag vurderer/benytter:<p>
        """

        yourBankId = get_user_bsu_bank_id(usr)
        productType = 'banksparing'
        product = 'bsu'
        for x in range(len(bsu_data)):
            seletectedBankId = bsu_data[x][1]
            url_change_bsu_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = email_strings(bsu_data[x][2])

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % bsu_data[x][7] + """%. <a href='""" + bsu_data[x][3] + """'>""" + bank_name + """</a>. SÃ¸k om Ã¥ bytte til """ + bank_name + """: """ + url_change_bsu_bank + """</p>
            """

        email_content += """<p><br></p>"""

    ## Adding savings account-data
    if not savings_account_data == '':
        email_content += """
          <b>Sparekonto / Innskuddskonto:</b> Finansvarsel har registrert """ + number_of_savings_banks + """ kontoer i norske banker med bedre rentevilkÃ¥r enn banken du i dag vurderer/benytter:<br>
        """

        yourBankId = get_user_savings_bank_id(usr)
        productType = 'banksparing'
        product = 'bankinnskudd'
        for x in range(len(savings_account_data)):
            seletectedBankId = savings_account_data[x][1]
            url_change_bsu_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

            bank_name = email_strings(savings_account_data[x][2])

            email_content += """
              <p>""" + str(x + 1) + """. Rente: %.2f""" % savings_account_data[x][7] + """%. <a href='""" + savings_account_data[x][3] + """'>""" + bank_name + """</a>. SÃ¸k om Ã¥ bytte til """ + bank_name + """: """ + url_change_bsu_bank + """</p>
            """


    email_content += """
      <p>Tusen takk for at du benytter Finansvarsel som er utviklet av Fredrik Bakken. Prosjektet hadde ikke vÃ¦rt mulig uten dataene <a href='https://www.finansportalen.no'>Finansportalen</a> tilbyr.<br></p>
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
    #server.sendmail(FROM, TO, MESSAGE.as_string())
    server.quit()

    print('Email to ' + TO + ' has been sent.')
