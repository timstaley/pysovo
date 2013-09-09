#!/usr/bin/python


#Minimal imports here - ensures proper testing of alert_response.
#(If not careful you might temporarily fix a broken import - which then remains broken)
from pysovo.tests.resources import datapaths
import alert_response as ar
import voeparse
##We bind the email sender to a dummy function:
ar.ps.comms.email.send_email = ar.ps.comms.email.dummy_email_send_function
ar.notification_email_prefix = "[TEST] " + ar.notification_email_prefix
ar.notify_contacts = [ ar.contacts['test']  ]  # Only notify test contacts
ar.contacts['ami']['email'] = 'DUMMY' + ar.contacts['ami']['email'] #Do NOT email AMI
ar.default_archive_root = "./"

def main():
    ar.voevent_logic(ar.voeparse.load(datapaths.swift_bat_grb_pos_v2))
    ##Now test one with null follow-up:
    ar.voevent_logic(ar.voeparse.load(datapaths.swift_bat_grb_low_dec))
    ##Now test one with bad star tracking:
    ar.voevent_logic(ar.voeparse.load(datapaths.swift_bat_grb_lost_lock))
    ar.voevent_logic(ar.voeparse.load(datapaths.swift_bat_known_source))

if __name__ == "__main__":
    main()
