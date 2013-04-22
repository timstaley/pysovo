#!/usr/bin/python


#Minimal imports here - ensures proper testing of alert_response.
#(If not careful you might temporarily fix a broken import - which then remains broken)
from pysovo.tests.resources import datapaths
import alert_response as ar

##We bind the email sender to a dummy function:
ar.ps.comms.email.send_email = ar.ps.comms.email.dummy_email_send_function

def main():
    ar.contacts['ami']['email'] = ar.contacts['test']['email'] #Do NOT email AMI
    ar.ps.observatories.ami.default_action = "CHECK" #And don't request an observation.


    ar.notify_contacts = [ ar.contacts['test']  ]  # Only notify test contacts
    ar.notification_email_subject = "[TEST] " + ar.notification_email_subject

    ar.default_archive_root = "./"


    test_packet = ar.voeparse.load(datapaths.swift_bat_grb_pos_v2)
    print "Packet loaded, ivorn", test_packet.attrib['ivorn']
    print "Logic go!"
    ar.voevent_logic(test_packet)

if __name__ == "__main__":
    main()
