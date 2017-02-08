# coding: utf-8
with (open("gmailpassword.txt")) as f:
    gmail_user = "NAISTGSK"
    gmail_pass = f.readline().splitlines()

import re

def is_NAIST_address(emailaddress):
    pattern = re.compile("@.s\.naist\.jp")
    res = re.search(pattern, emailaddress)
    if res: return True
    else: return False

def get_emails():
    import poplib
    import email
    from email import parser

    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(gmail_user)
    pop_conn.pass_(gmail_pass)
    # Get messages from server:
    messages0 = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    messagesB = [b"\n".join(mssg[1]) for mssg in messages0]
    # Parse message intom an email object:
    messages = [email.message_from_bytes(mssg) for mssg in messagesB]
    pop_conn.quit()

    # Check if the addresses are already in the list
    import pickle
    regdmails = pickle.load( open( "naistvoting-addresslog2016.p", "rb" ) )
    newmails = []
    for message in messages:
        if is_NAIST_address(message['from']):
            m = message['from']
            start = m.find('<')+1
            end = m.find('>', start)
            address = m[start:end]
            if not address in regdmails:
                newmails.append(address)
                regdmails.append(address)
                print("Added " + address)

    pickle.dump( regdmails, open( "naistvoting-addresslog2016.p", "wb" ) )
    return newmails

# Just sends an email to a recipient from my email address.
# From http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
# Then adapted for japanese:
def send_email(recipient, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    import traceback

    FROM = 'NAIST学生会 / Student Association'
    FROM = Header(FROM, 'utf-8').encode()
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    #### MIMEText alternative try
    msg = MIMEText(body.encode('utf-8'), _charset='utf-8')
    # msg = MIMEText(body.encode('utf-8'), 'plain',  'utf-8')   #Both seems to work
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")
        traceback.print_exc()
