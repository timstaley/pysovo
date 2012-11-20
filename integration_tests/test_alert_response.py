#!/usr/bin/python

import sys
import functools
#Don't import anything here - prevents proper testing of alert_response.
#(You might temporarily fix a broken import - which then remains broken)
from pysovo.tests.resources import datapaths
from pysovo.observatories import ami_module
import voeparse
import alert_response as ar

def main():
    ar.obs.ami.email_address = ar.ps.address_book.test.email #Do NOT email AMI
    ar.obs.ami.default_action = "CHECK" #And don't request an observation.
    ar.obs.ami.internal_request_mechanism = functools.partial(
                       ami_module.email_ami,
                       subject="[TEST] " + ami_module.request_email_subject
                       )

    ar.notify_contacts = [ ar.ps.address_book.tim  ]  # Only notify test contacts
    ar.notification_email_subject = "[TEST] " + ar.notification_email_subject

    ar.default_archive_root = "./"


    test_packet = voeparse.load(datapaths.swift_bat_grb_pos_v2)
    print "Packet loaded, ivorn", test_packet.attrib['ivorn']

    ar.voevent_logic(test_packet)

if __name__ == "__main__":
    main()
