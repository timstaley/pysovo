#!/usr/bin/env python
import logging
import time
from pysovo.comms import email
from pysovo.local import contacts
logging.basicConfig(level=logging.DEBUG)

def main():
    test_message= """Test 1 - single recipient"""
    start = time.clock()
    email.send_email(recipient_addresses=contacts.test_contacts[0].email,
                    subject="Python email test",
                    body_text=test_message)
    end = time.clock()
    elapsed = end - start
    print "First send took", elapsed, "seconds."
    
    test_message= """Test 2 - multiple recipients"""

    start = time.clock()
    email.send_email(recipient_addresses=[c.email for c in contacts.test_contacts],
                    subject="Python email test",
                    body_text=test_message)
    end = time.clock()
    elapsed = end - start
    print "Second send took", elapsed, "seconds."


if __name__ == "__main__":
    main() 
