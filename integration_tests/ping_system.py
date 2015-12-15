#!/usr/bin/env python
"""
Pings a live broker / alert_response setup with test packet.
This provides a means of testing a live system in a safe and unobtrusive manner.
"""
import datetime
import logging
import voeventparse
import pysovo
import pysovo.voevent
from pysovo.local import contacts
from pysovo.formatting import datetime_format_short
from pysovo.triggers import test_trigger_substream


def main():
    now = datetime.datetime.utcnow()
    test_packet = pysovo.voevent.create_skeleton_4pisky_voevent(
        substream=test_trigger_substream,
        stream_id=now.strftime(datetime_format_short),
        role=voeventparse.definitions.roles.test,
        date=now,
    )

    print "Sending packet, ivorn: ", test_packet.attrib['ivorn']
    broker = contacts.local_vobroker
    before = datetime.datetime.utcnow()
    pysovo.comms.comet.send_voevent(test_packet, broker.ipaddress, broker.port)
    after = datetime.datetime.utcnow()
    print "Done. Sending took", (after - before).total_seconds(), "seconds."

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
