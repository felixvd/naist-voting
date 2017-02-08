# coding: utf-8

import requests
from mailfuncs import *

with open("mytoken") as f:
    #ACCESSTOKEN = f.read().rstrip('\n')
    ACCESSTOKEN = '-LlA-pjLiu9CMRwGafF3shiAX1rpZ.JacUpEVJrYA.p-xuQ8U1EE15VdGIGoMFXTDAGd0Imhq5eYqiA2swEPVIO7B7LHh1ru0IZ9ltNcIZ8wj3byi0izeqhNw5pRP3Ab'

# Creates a message in a collector on Surveymonkey with recipients and sends it out
def send_invites(newmails, surveyid, collid):
    # Connection to Surveymonkey
    # ACCESSTOKEN = 'secret~~'
    s = requests.Session()
    s.headers.update({
      "Authorization": "Bearer %s" % ACCESSTOKEN,
      "Content-Type": "application/json"   })

    ## This is the template data for the new message
    # The collector is obsolete.
    collpayload = {
        'type':'email',
        'sender_email': 'naistgsk@gmail.com',
        #'edit_response_type': 'never',
        'close_date': '2017-02-13T05:00:00+00:00',
        'name': 'Auto-Sendout',
        #'anonymous_type': 'fully_anonymous'
    }

    msgpayload = {
        'type':'invite',
        'body_html': '<html>\n<body style="margin:0; padding: 0;">\n<div align="center">\n   <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%"\n          style="font-family: Arial,Helvetica,sans-serif; max-width: 700px;">\n       <tr bgcolor="#2c7db7">\n           <td colspan="5" height="40">\xa0</td>\n       </tr>\n       <tr bgcolor="#2c7db7">\n           <td width="20">\xa0</td>\n           <td width="20">\xa0</td>\n           <td align="center" style="font-size: 29px; color:#FFFFFF; font-weight: normal; letter-spacing: 1px; line-height: 1;\n                           text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.2); font-family: Arial,Helvetica,sans-serif;">\n              NAIST Student Life Survey / NAIST 学生生活サーベイ\n           </td>\n           <td width="20">\xa0</td>\n           <td width="20">\xa0</td>\n       </tr>\n       <tr bgcolor="#2c7db7">\n           <td colspan="5" height="40">\xa0</td>\n       </tr>\n       <tr>\n           <td height="10" colspan="5">\xa0</td>\n       </tr>\n       <tr>\n           <td>\xa0</td>\n           <td colspan="3" align="left" valign="top" style="color:#666666; font-size: 13px;">\n              {% if FirstQuestion %}\n                <p>{{EmbeddedBody}}</p>\n              {% else %}\n                <p>Thank you for taking part in the survey. Remember that you can\xa0be frank\xa0- your answers and comments are confidential.<br><br>The survey ends at noon on Monday, February 13. Thank you for your time.<br><br>サーベイを参加していただきありがとうございます。アンケートの回答は機密に管理いたしますので、率直なご意見をお願いします。<br><br>サーベイは月曜日2月13 日12時までです。宜しくお願いします。<br><br>NAIST学生会から<br>From the NAIST Student Association</p>\n              {% endif %}\n           </td>\n           <td>\xa0</td>\n       </tr>\n\n       {% if FirstQuestion %}\n           <tr>{{FirstQuestion}}</tr>\n       {% else %}\n           <tr>\n               <td colspan="5" height="30">\xa0</td>\n           </tr>\n           <tr>\n               <td>\xa0</td>\n               <td colspan="3">\n                   <table border="0" cellpadding="0" cellspacing="0" align="center"\n                          style="background:#2c7db7; border-radius: 4px; border: 1px solid #BBBBBB; color:#FFFFFF; font-size:14px; letter-spacing: 1px; text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.8); padding: 10px 18px;">\n                       <tr>\n                           <td align="center" valign="center">\n                               <a href="{{SurveyLink}}" target="_blank"\n                                  style="color:#FFFFFF; text-decoration:none;">Begin Survey / サーベイを始める</a>\n                           </td>\n                       </tr>\n                   </table>\n               </td>\n               <td>\xa0</td>\n           </tr>\n           <tr>\n               <td colspan="5" height="30">\xa0</td>\n           </tr>\n       {% endif %}\n       <tr valign="top" style="color: #666666;font-size: 10px;">\n           <td>\xa0</td>\n           <td valign="top" align="center" colspan="3">\n               <p>Please do not forward this email as its survey link is unique to you. <br><a href="{{OptOutLink}}" target="_blank" style="color: #333333; text-decoration: underline;">Unsubscribe</a> from this list</p>\n           </td>\n           <td>\xa0</td>\n       </tr>\n       <tr>\n           <td height="20" colspan="5">\xa0</td>\n       </tr>\n\n       <tr style="color: #999999;font-size: 10px;">\n           <td align="center" colspan="5">{{FooterHTML}}</td>\n       </tr>\n       <tr>\n           <td height="20" colspan="5">\xa0</td>\n       </tr>\n   </table>\n</div>\n</body>\n</html>',
        'subject': 'NAIST Student Council Survey     NAIST学生会学生生活サーベイ'
    }

    print("Inviting into collector")

    ##  1) Create a message in the collector
    url = "https://api.surveymonkey.net/v3/collectors/%s/messages" % (collid)
    r = s.post(url, json=msgpayload)
    msgid = r.json()['id']

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

    ## 3) Send it all out
    url = "https://api.surveymonkey.net/v3/collectors/%s/messages/%s/send" % (collid, msgid)
    r = s.post(url, json={})

    print("Sent out invites")
    return r


### The main script
import datetime
import time
newmails = get_emails()
#newmails = ['fvdrigalski@gmail.com']
surveyid = '113230078'     # Student Life Survey
collectorid = '153163302'  # Student Life Autocollector

# # To start off on day 1:
# import pickle
# regdmails = pickle.load( open( "naistvoting-addresslog2016.p", "rb" ) )
# newmails = regdmails

# logfilename = "/home/felix/naist-voting/naistvoting-logfile.txt"
logfilename = "./naistvoting-logfile.txt"

if newmails:
    with open(logfilename, "a") as myfile:
        st = datetime.datetime.utcnow()
        myfile.write("Found " + str(len(newmails)) + " mails at " + str(st) + "\n")

    for mail in newmails:
        send_email(mail, 'Your survey link has been sent / サーベイリンク送信', 'Your link for the NAIST Student Life Survey has been sent out. If you do not receive a personalized link from Surveymonkey shortly, please check your Spam folder or contact us. Thank you for your participation! \n \nNAIST学生生活サーベイリンクを送りました。Surveymonkeyから個人リンクが送られませんなら、ご連絡ください。ご協力ありがとうございます！')
        time.sleep(1)       # Otherwise large amounts of mails kill the server connection
    with open(logfilename, "a") as myfile:
        st = datetime.datetime.utcnow()
        myfile.write("Sent out the email alerts via gmail. Now trying to invite. \n")
    res = send_invites(newmails, surveyid, collectorid)
    if not res:
        send_email('naistgsk@gmail.com', 'Oh fuck', 'Something went wrong with the Surveymonkey script')

    # Logging
    with open(logfilename, "a") as myfile:
        st = datetime.datetime.utcnow()
        myfile.write("Sent out invites to " + str(len(newmails)) + " addresses at " + str(st) + "\n")
        for line in newmails:
            myfile.write(line + "\n")
        myfile.write("\n --- \n")

else:
    print("No new addresses were seen.\n --- \n")
