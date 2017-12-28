import smtplib

from settings import url_change_bank, email_credentials

def format_email(user, bsu_data):
    complete_body = ''

    firstname = user[0]
    lastname = user[1]
    hello_message = 'Hei ' + firstname + ' ' + lastname + ',\n\n'

    number_of_bsu_banks = str(len(bsu_data))
    bsu_message = 'Finansvarsel har registrert ' + number_of_bsu_banks + ' BSU-kontoer i norske banker med bedre rentevilkaar enn banken du i dag vurderer/benytter:\n'

    bsu_banks = ''
    for x in range(len(bsu_data)):
        yourBankId = user[8]
        seletectedBankId = bsu_data[x][1]
        productType = 'banksparing'
        product = 'bsu'
        url_change_bsu_bank = url_change_bank + '?yourBankId=' + yourBankId + '&selectedBankId=' + seletectedBankId + '&productType=' + productType + '&product=' + product

        bank_name = bsu_data[x][2].replace('Æ', 'Ae').replace('æ', 'ae').replace('Ø', 'Oe').replace('ø', 'oe').replace('Å', 'Aa').replace('å', 'aa')

        bsu_bank = str(x + 1) + '. Rente: %.2f' % bsu_data[x][7] + '%. ' + bank_name + ' (' + bsu_data[x][3] + '). Onsker du aa bytte til denne banken? Folg lenken: ' + url_change_bsu_bank + '\n'

        bsu_banks += bsu_bank

    thank_you_message = '\nTusen takk for at du benytter Finansvarsel som er utviklet av Fredrik Bakken. Prosjektet hadde ikke vaert mulig uten den dataen Finansportalen (https://www.finansportalen.no) tilbyr.\n\n'

    from_message = 'Med vennlig hilsen,\nFinansvarsel'

    complete_body = hello_message + bsu_message + bsu_banks + thank_you_message + from_message

    return complete_body


def send_email(recipient, subject, body):
    FROM = email_credentials()[0]
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("send.one.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email_credentials()[0], email_credentials()[1])
        server.sendmail(FROM, TO, message)
        server.close()
        print('Successfully sent the mail')
    except:
        print("Failed to send mail")
