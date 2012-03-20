#!/usr/bin/python

import sys
from VOEventLib import VOEvent as voe, Vutil as voe_utils
import functools
import pysovo as ps
import pysovo.observatories as obs
import pysovo.observatories.ami_module as ami_details
import alert_response

def main():
    obs.ami.email_address = ps.address_book.test.email #Do NOT email AMI
    obs.ami.default_action = "CHECK" #Insurance.
    obs.ami.internal_request_mechanism = functools.partial(ami_details.email_ami, 
                                                           subject = "[TEST] "+ami_details.request_email_subject)
    
    alert_response.notify_contacts =[ ps.address_book.tim  ]  # Only notify test contacts
    alert_response.notification_email_subject = "[TEST] " + alert_response.notification_email_subject
    
     
    
    test_packet = voe_utils.parse("../test_data/BAT_GRB_Pos_517234-259.xml")
    
    alert_response.voevent_logic(test_packet)
        
if __name__ == "__main__":
    main() 