#pysovo VOEvent Tools
#Tim Staley 2012
#Based on various web snippets.

import json
import os
import sys
import getpass
import smtplib
import base64

import pysovo as ps
import logging
logger = logging.getLogger(__name__)


class EmailConfigKeys():
    username = 'username'
    password = 'password'
    smtp_server = 'smtp_server'
    smtp_port = 'smtp_port'


keys = EmailConfigKeys()

def prompt_for_config(config_filename=ps.default_email_config_file):
    while os.path.exists(config_filename):
        print "Email account file already exists at ", config_filename
        raw_input("Please delete it then press a key to continue\n"
                  "(or CTRL-C to abort)")

    default_smtp_server = "smtp.googlemail.com"
    default_smtp_port = 587
    ps.utils.ensure_dir(config_filename)
    outputfile = open(config_filename, 'w')

    account = {}

    print "Please enter the smtp server address:"
    print "(Default = {dserve})".format(dserve=default_smtp_server)
    account[keys.smtp_server] = raw_input(">")
    if account[keys.smtp_server] == "":
        account[keys.smtp_server] = default_smtp_server

    print "Please enter the smtp server port:"
    print "(Default = {dport})".format(dport=default_smtp_port)
    account[keys.smtp_port] = raw_input(">")
    if account[keys.smtp_port] == "":
        account[keys.smtp_port] = default_smtp_port

    print "Please enter the smtp username: (e.g. someone@gmail.com)"
    account[keys.username] = raw_input(">")

    print "Now please enter your password:"
    rawpass = getpass.getpass()
    account[keys.password] = base64.b64encode(rawpass)
    print "You entered:"
    print "Server", account[keys.smtp_server]
    print "Port", account[keys.smtp_port]
    print "User", account[keys.username]
    print "Pass", "(Not shown)"

    outputfile.write(json.dumps(account, indent=1))
    outputfile.close()
    print ""
    print "Account settings saved to:", config_filename

    chmod_command = "chmod go-rwx {file}".format(file=config_filename)
    os.system(chmod_command)

    return config_filename

def load_account_settings_from_file(config_filename=ps.default_email_config_file):
    #print "Loading email acc from ", config_filename
    try:
        with open(config_filename, 'r') as config_file:
            account = json.loads(config_file.read())
    except IOError:
        logger.exception("Error: Could not load email account settings")
        raise

    return account

def send_email(account,
                recipient_addresses,
                subject,
                body_text,
                verbose=False
                ):
    if verbose:
        print "Loaded account, starting SMTP session"

    recipient_addresses = ps.utils.listify(recipient_addresses)

    smtpserver = smtplib.SMTP(account[keys.smtp_server],
                              account[keys.smtp_port])
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(account[keys.username],
                     base64.b64decode(account[keys.password]))

    sender = account[keys.username]

    recipients_str = ",".join(recipient_addresses)
    if verbose:
        print "Logged in, emailing", recipients_str
    header = "".join(['To: ', recipients_str, '\n',
                        'From: ', sender, '\n',
                        'Subject: ', subject, '\n'])

    msg = "".join([header, '\n',
                    body_text, '\n\n'])
    smtpserver.sendmail(sender, recipient_addresses, msg)
    if verbose:
        print 'Message sent'
    smtpserver.close()
    pass

def dummy_email_send_function(account,
                recipient_addresses,
                subject,
                body_text,
                verbose=False
                ):
    print "*************"
    print "Would have sent an email to:"
    print ps.utils.listify(recipient_addresses)
    print "Subject:", subject
    print "--------------"
    print body_text
    print "*************"

