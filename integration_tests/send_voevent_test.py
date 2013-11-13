#!/usr/bin/python
from __future__ import absolute_import
import logging
# Minimal imports here - ensures proper testing of alert_response.
# (If not careful you might temporarily fix a broken import - which then remains broken)
from pysovo.tests.resources import datapaths
from pysovo.comms.comet import send_voevent
from pysovo.local import contacts
import voeparse

logging.basicConfig(level=logging.DEBUG)


def main():
    test_pkt = voeparse.Voevent(stream='voevent.astro.soton/TEST',
                                   stream_id=4,
                                   role=voeparse.roles.test)

    send_voevent(test_pkt, host=contacts['sendbroker']['hostname'])

if __name__ == "__main__":
    main()
