#pysovo VOEvent Tools
#Tim Staley, <timstaley337@gmail.com>, 2012

import simplejson as json
import os
import sys
import getpass
import warnings

import time
import glob
import httplib
import urllib

import quick_keys as keys
import pysovo.utils as utils
        
default_sms_config_file="".join((os.environ['HOME'], "/.vo_alerts/sms_acc"))

try:        
    import textmagic
    import textmagic.client
    sms_available = True
except ImportError:
    warnings.warn( "NB textmagic not found, SMS alerts not available.", ImportWarning)
    sms_available = False
        

# http://api.textmagic.com/https-api/sms-delivery-notification-codes
delivery_status_key={
                     'q': 'Queued',
                     'u': 'Unknown',
                     'r': 'Sent',
                     'd': 'Delivered',
                     'e': 'Send error',  
                     'f': 'Delivery error' #Different to send error?
                     }

        
def prompt_for_config( config_filename = default_sms_config_file ):
    utils.ensure_dir(config_filename)
    outputfile=open(config_filename, 'w')
    
    account = {}
    print "Please enter the sms username:"
    account[keys.sms_account.username]= raw_input(">")
    
    print "Now please enter your API password:"
    account[keys.sms_account.api_password]= raw_input(">")
    
    print "You entered:"
    print "User", account[keys.sms_account.username]
    print "API Pass", account[keys.sms_account.api_password]
    
    outputfile.write(json.dumps(account))
    outputfile.close()
    print ""
    print "Account settings saved to:", config_filename
    
    chmod_command = "chmod go-rwx {file}".format(file=config_filename)
    os.system(chmod_command)
    
    return config_filename

def load_account_settings_from_file( config_filename = default_sms_config_file):
    if sms_available:
        try:
            with open(config_filename, 'r') as config_file:
                account = json.loads(config_file.read())
        except Exception:
            print "Error: Could not load email account from "+ config_filename
            raise 
        return account
    else:
        return None

def send_sms( account,
                recipients,
                body_text,
                debug=False
                ):    
    if debug:
        print "Loaded account, starting SMS session"
        if len(body_text) > 155:
            print "Warning: Body text will be truncated"
            
    body_text=body_text[:160]

    client = textmagic.client.TextMagicClient(
                  account[keys.sms_account.username], 
                  account[keys.sms_account.api_password])
            
    result=  client.send(body_text, recipients)

    message_ids = result['message_id'].keys()
    return message_ids

def check_sms_statuses(account, message_ids):
    client = textmagic.client.TextMagicClient(
                  account[keys.sms_account.username], 
                  account[keys.sms_account.api_password])
    
    responses = client.message_status(message_ids)
    delivery_status_codes = [ responses[id]['status'] for id in message_ids]
    
    delivery_statuses =[]
    for code in delivery_status_codes:
        if code in delivery_status_key:
            delivery_statuses.append(delivery_status_key[code])
        else:
            delivery_statuses.append(code)
    
    return zip(message_ids, delivery_status_codes, delivery_statuses)




def check_sms_balance(account, debug=False):
    client = textmagic.client.TextMagicClient(
                      account[keys.sms_account.username], 
                      account[keys.sms_account.api_password])
    
    balance = client.account()['balance']
    if debug:
        print "Balance is:", balance
        
    return balance


