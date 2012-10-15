#!/usr/bin/python

import sys
import functools
import pysovo as ps
import pysovo.voevent
import pysovo.observatories as obs
import pysovo.observatories.ami_module as ami_details
from pysovo.tests.resources import datapaths
import alert_response

def main():
    obs.ami.email_address = ps.address_book.test.email #Do NOT email AMI
    obs.ami.default_action = "CHECK" #And don't request an observation.
    obs.ami.internal_request_mechanism = functools.partial(
                       ami_details.email_ami,
                       subject="[TEST] " + ami_details.request_email_subject
                       )

    alert_response.notify_contacts = [ ps.address_book.tim  ]  # Only notify test contacts
    alert_response.notification_email_subject = "[TEST] " + alert_response.notification_email_subject



    test_packet = ps.voevent.build.from_file(datapaths.swift_bat_grb_pos_v2)
    print "Packet loaded, ivorn", test_packet.attrib['ivorn']

    alert_response.voevent_logic(test_packet)

if __name__ == "__main__":
    main()
