import simplejson as json
import os
import sys
import getpass
import smtplib
import _quick_keys as keys
import _internal_utils as utils
        
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
    except Exception:
        print "Error: Could not load email account from "+ config_filename
        raise 
    
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



