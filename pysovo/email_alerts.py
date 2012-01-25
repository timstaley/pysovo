import simplejson as json
import os
import sys
import getpass
import smtplib
import _quick_keys as keys
import _utils as utils
        
default_email_config_file="".join((os.environ['HOME'], "/.vo_alerts/email_acc"))

        
def prompt_for_config( config_filename = default_email_config_file ):
    default_smtp_server = "smtp.googlemail.com"
    default_smtp_port = 587
    utils.ensure_dir(config_filename)
    outputfile=open(config_filename, 'w')
    
    account = {}
    
    print "Please enter the smtp server address:" 
    print "(Default = {dserve})".format(dserve=default_smtp_server)
    account[keys.email_account.smtp_server]= raw_input(">")
    if account[keys.email_account.smtp_server]=="":
        account[keys.email_account.smtp_server] = default_smtp_server
        
    print "Please enter the smtp server port:"
    print "(Default = {dport})".format(dport=default_smtp_port)
    account[keys.email_account.smtp_port]= raw_input(">")
    if account[keys.email_account.smtp_port]=="":
        account[keys.email_account.smtp_port] = default_smtp_port
   
    print "Please enter the smtp username:"
    account[keys.email_account.username]= raw_input(">")
    
    print "Now please enter your password:"
    account[keys.email_account.password]= getpass.getpass()
    
    print "You entered:"
    print "Server", account[keys.email_account.smtp_server]
    print "Port", account[keys.email_account.smtp_port]
    print "User", account[keys.email_account.username]
    print "Pass", "(Not shown)"
    
    outputfile.write(json.dumps(account))
    outputfile.close()
    print ""
    print "Account settings saved to:", config_filename
    
    chmod_command = "chmod go-rwx {file}".format(file=config_filename)
    os.system(chmod_command)
    
    return config_filename

def load_account_settings_from_file( config_filename = default_email_config_file):
    try:
        with open(config_filename, 'r') as config_file:
            account = json.loads(config_file.read())
    except Exception as e:
        print "Error: Could not load email account"
        sys.exit()
    return account

def send_email( account,
                recipient,
                subject,
                body_text,
                debug=False
                ):    
    if debug:
        print "Loaded account, starting SMTP session"
    
    smtpserver = smtplib.SMTP(account[keys.email_account.smtp_server],
                              account[keys.email_account.smtp_port])
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(account[keys.email_account.username], 
                     account[keys.email_account.password])
    if debug:
        print "Logged in"
        
    sender = account[keys.email_account.username]
    header = "".join( ['To: ',recipient,'\n',
                        'From: ',sender,'\n',
                        'Subject: ', subject,'\n'])
    
    msg = "".join( [header,'\n',
                    body_text,'\n\n'])
    smtpserver.sendmail(sender, recipient, msg)
    if debug:
        print 'Message sent'
    smtpserver.close()
    pass

def format_ami_alert(array,
                    target,
                    ra,
                    dec,
                    timing,
                    duration,
                    requester,
                    comment,
                    action):
    
#      Array=     AMI-SA
#  Target=    GRB110328A
#  J2000RA=   16 44 49.93
#  J2000Dec=  57 35 59.1
#  Timing=    ST 15.45
#  Duration=  02.00
#  Requester= djt
#  Comment=   Target of Opportunity test
#
#where:
#
# 'Array'     must be either 'AMI-SA' or 'AMI-LA'.
# 'Target' and the J2000 coordinates define the observation target.
# 'Timing'    specifies the start of the observation, either by Local
#             Sidereal Time 'ST hh.mm', or by using one of the keywords
#             'Transit' (to observe through transit) or 'ASAP' (to start
#             the observation as soon as possible).
# 'Duration'  specifies the length of the observation (hh.mm).
# 'Requester' identifies the observer.
# 'Comment'   adds a string of comment text to the observation header.

    alert_text = "".join(["Array=     ",array,"\n",
                "Target=    ", target, "\n"
                "J2000RA=   ", ra,"\n",
                "J2000Dec=  ", dec, "\n",
                "Timing=    ", timing, "\n",
                "Duration=  ", duration, "\n",
                "Requester= ", requester, "\n",
                "Comment=  ", comment, "\n"
                "Action=  ", action, "\n"
                ])
    return alert_text

