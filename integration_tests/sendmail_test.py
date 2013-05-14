#!/usr/bin/python

from pysovo.comms import email
from pysovo.local import contacts

def main():
    account = email.load_account_settings_from_file()

    test_message= """Test 1 - single recipient"""
    email.send_email(account,
                     recipient_addresses=contacts['test']['email'],
                     subject="Python email test",
                     body_text=test_message,
                     verbose=True)
    
    
    test_message= """Test 2 - multiple recipients"""
    
    email.send_email(account,
    #                        recipients= address_book.email_addresses["test"],
                     recipient_addresses=[ contacts['tim']['email'],
                                          contacts['test']['email']],
                     subject="Python email test",
                     body_text=test_message,
                     verbose=True)
    
    print "Test completed"


if __name__ == "__main__":
    main() 
