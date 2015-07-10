#!/usr/bin/env python
from __future__ import absolute_import
import logging
logging.basicConfig(level=logging.DEBUG)

#Minimal imports here - ensures proper testing of alert_response.
#(If not careful you might temporarily fix a broken import - which then remains broken)
from pysovo.tests.resources import datapaths
import alert_response as ar
##We bind the email sender to a dummy function:
ar.ps.comms.email.send_email = ar.ps.comms.email.dummy_email_send_function
ar.ps.comms.comet.send_voevent = ar.ps.comms.comet.dummy_send_to_comet_stub
ar.notification_email_prefix = "[TEST] " + ar.notification_email_prefix
ar.grb_contacts = ar.contacts.test_contacts  # Only notify test contacts
ar.amiobs.email_address = 'blocked!' + ar.amiobs.email_address  # Do NOT email AMI
ar.default_archive_root = "./"

def main():
    def test_packet(path):
        with open(path) as f:
            ar.voevent_logic(ar.voeventparse.load(f))
    print "Sometimes visible source:"
    test_packet(datapaths.swift_bat_grb_pos_v2)
    ##Now a circumpolar source:
    print "Always visible source:"
    test_packet(datapaths.swift_bat_grb_circumpolar)
    ##Now test one with null follow-up:
    print "Never visible source:"
    test_packet(datapaths.swift_bat_grb_low_dec)
    ##Now test one with bad star tracking:
    print "Bad source:"
    test_packet(datapaths.swift_bat_grb_lost_lock)
    print "Known source:"
    test_packet(datapaths.swift_bat_known_source)

if __name__ == "__main__":
    main()
