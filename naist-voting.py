# coding: utf-8

#Function definitions

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
    pop_conn.user('NAISTStudentCouncil')
    pop_conn.pass_('SECRET')
    #Get messages from server:
    messages0 = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    messagesB = [b"\n".join(mssg[1]) for mssg in messages0]
    #Parse message intom an email object:
    #messages = [parser.Parser().parsestr(mssg) for mssg in messages1]
    messages = [email.message_from_bytes(mssg) for mssg in messagesB]
#     for message in messages:
#         print(message['subject'])
    pop_conn.quit()

    # Extract all unique NAIST mails from the stack
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
    import traceback

    gmail_user = 'NAISTStudentCouncil'
    gmail_pwd = 'SECRET'
    FROM = 'NAISTStudentCouncil'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    #### MIMEText alternative try
    msg = MIMEText(body.encode('utf-8'), _charset='utf-8')
#     msg['Subject'] = subject
#     msg['From'] = FROM
#     msg['To'] = TO
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
#         server.sendmail(FROM, TO, message)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")
        traceback.print_exc()

# Creates a message in a collector on Surveymonkey with recipients and sends it out
def send_invites(newmails, surveyid, collid):
    # Connection to Surveymonkey
    ACCESSTOKEN = 'SECRET'
    import requests
    s = requests.Session()
    s.headers.update({
      "Authorization": "Bearer %s" % ACCESSTOKEN,
      "Content-Type": "application/json"   })

    ## This is the template data for the new message
    # The collector is obsolete.
    collpayload = {
        'type':'email',
        'sender_email': 'naiststudentcouncil@gmail.com',
        'edit_response_type': 'never',
        'close_date': '2017-01-30T15:00:00+00:00',
        'name': 'Auto-Sendout',
        'anonymous_type': 'fully_anonymous'
    }

    msgpayload = {
        'type':'invite',
        'body_html': '<html>\n<body style="margin:0; padding: 0;">\n<div align="center">\n   <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%"\n          style="font-family: Arial,Helvetica,sans-serif; max-width: 700px;">\n       <tr bgcolor="#2c7db7">\n           <td colspan="5" height="40">\xa0</td>\n       </tr>\n       <tr bgcolor="#2c7db7">\n           <td width="20">\xa0</td>\n           <td width="20">\xa0</td>\n           <td align="center" style="font-size: 29px; color:#FFFFFF; font-weight: normal; letter-spacing: 1px; line-height: 1;\n                           text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.2); font-family: Arial,Helvetica,sans-serif;">\n              NAIST Student Council Election 2016/2017   2016年度 NAIST学生会代表選挙\n           </td>\n           <td width="20">\xa0</td>\n           <td width="20">\xa0</td>\n       </tr>\n       <tr bgcolor="#2c7db7">\n           <td colspan="5" height="40">\xa0</td>\n       </tr>\n       <tr>\n           <td height="10" colspan="5">\xa0</td>\n       </tr>\n       <tr>\n           <td>\xa0</td>\n           <td colspan="3" align="left" valign="top" style="color:#666666; font-size: 13px;">\n              {% if FirstQuestion %}\n                <p>{{EmbeddedBody}}</p>\n              {% else %}\n                <p>This is your personalized link for the\xa0NAIST Student Council Election 2016/2017. Do not pass it on to anyone else.\xa0You can only cast your vote(s) once.\xa0<br><br>Please click the button below to go\xa0to the vote. Do not forget to read about the candidates here:\xa0https://goo.gl/LNN3jg<br><br>これはあなたの投票の個人リンクです。他の人に渡さないでください。一回だけ投票できます(3票まで)。<br><br>下のボタンをクリックすると投票に進みます。この前、立候補者の自己紹介をお読みください：https://goo.gl/LNN3jg</p>\n              {% endif %}\n           </td>\n           <td>\xa0</td>\n       </tr>\n\n       {% if FirstQuestion %}\n           <tr>{{FirstQuestion}}</tr>\n       {% else %}\n           <tr>\n               <td colspan="5" height="30">\xa0</td>\n           </tr>\n           <tr>\n               <td>\xa0</td>\n               <td colspan="3">\n                   <table border="0" cellpadding="0" cellspacing="0" align="center"\n                          style="background:#2c7db7; border-radius: 4px; border: 1px solid #BBBBBB; color:#FFFFFF; font-size:14px; letter-spacing: 1px; text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.8); padding: 10px 18px;">\n                       <tr>\n                           <td align="center" valign="center">\n                               <a href="{{SurveyLink}}" target="_blank"\n                                  style="color:#FFFFFF; text-decoration:none;">Proceed to Vote / 投票へ進む</a>\n                           </td>\n                       </tr>\n                   </table>\n               </td>\n               <td>\xa0</td>\n           </tr>\n           <tr>\n               <td colspan="5" height="30">\xa0</td>\n           </tr>\n       {% endif %}\n       <tr valign="top" style="color: #666666;font-size: 10px;">\n           <td>\xa0</td>\n           <td valign="top" align="center" colspan="3">\n               <p>Please do not forward this email as its survey link is unique to you. <br><a href="{{OptOutLink}}" target="_blank" style="color: #333333; text-decoration: underline;">Unsubscribe</a> from this list</p>\n           </td>\n           <td>\xa0</td>\n       </tr>\n       <tr>\n           <td height="20" colspan="5">\xa0</td>\n       </tr>\n\n       <tr style="color: #999999;font-size: 10px;">\n           <td align="center" colspan="5">{{FooterHTML}}</td>\n       </tr>\n       <tr>\n           <td height="20" colspan="5">\xa0</td>\n       </tr>\n   </table>\n</div>\n</body>\n</html>',
        'subject': 'NAIST Student Council Election 2016/2017     2016年度 NAIST学生会代表選挙'
    }

    # ## 1) Make a new collector in the survey
    # url = "https://api.surveymonkey.net/v3/surveys/%s/collectors" % (surveyid)
    # r = s.post(url, json=collpayload)
    # collid = r.json()['id']
    # #r.json()


    print("Inviting into collector")

    ##  1.5) Make a message in the new automatic collector
    url = "https://api.surveymonkey.net/v3/collectors/%s/messages" % (collid)
    r = s.post(url, json=msgpayload)
    msgid = r.json()['id']
    #r.json()

    ## 2) Add the email recipients to the message
    if len(newmails) > 1:
        emails = []
        for mail in newmails:
            emails.append({"email":mail})
        url = "https://api.surveymonkey.net/v3/collectors/%s/messages/%s/recipients/bulk" % (collid, msgid)
        payload = {"contacts" :emails}
    else: # If len = 1
        url = "https://api.surveymonkey.net/v3/collectors/%s/messages/%s/recipients" % (collid, msgid)
        payload = {"email": newmails[0]}
    r = s.post(url, json=payload)
    #r.json()

    ## 3) Send it all out
    url = "https://api.surveymonkey.net/v3/collectors/%s/messages/%s/send" % (collid, msgid)
    r = s.post(url, json={})
    #r.json()

    print("Sent out invites")
    return r


### The main script
import datetime
newmails = get_emails()
#newmails = ['fvdrigalski@gmail.com', 'naiststudentcouncil@gmail.com']

# # To start off on day 1:
# import pickle
# regdmails = pickle.load( open( "naistvoting-addresslog2016.p", "rb" ) )
# newmails = regdmails

logfilename = "/home/felix/naist-voting/naistvoting-logfile.txt"

if newmails:
    with open(logfilename, "a") as myfile:
        st = datetime.datetime.utcnow()
        myfile.write("Found " + str(len(newmails)) + " mails at " + str(st) + "\n")

    for mail in newmails:
        send_email(mail, 'Your voting link has been sent / 投票リンク送信', 'Your voting link for the NAIST Student Council Election has been sent out. If you do not receive a personalized link from Surveymonkey shortly, please check your Spam folder or contact us. Thank you for voting! \n \n NAIST学生会投票リンク送りました。Surveymonkeyから個人リンクが送られませんなら、ご連絡ください。ご協力ありがとうございます！')
    with open(logfilename, "a") as myfile:
        st = datetime.datetime.utcnow()
        myfile.write("Sent out the email alerts via gmail. Now trying to invite. \n")
    res = send_invites(newmails, '113051556', '152800276')   ## The real survey
    #res = send_invites(newmails, '112695741')    ## The test survey
    if not res:
        send_email('naiststudentcouncil', 'Oh fuck', 'Something went wrong with the Surveymonkey script')

    # Logging
    with open(logfilename, "a") as myfile:
        st = datetime.datetime.utcnow()
        myfile.write("Sent out invites to " + str(len(newmails)) + " addresses at " + str(st) + "\n")
        for line in newmails:
            myfile.write(line + "\n")
        myfile.write("\n --- \n")

else:
    print("No new addresses were seen.\n --- \n")
