#!/usr/bin/env python
"""
Pings a live broker / alert_response setup with test packet.
This provides a means of testing a live system in a safe and unobtrusive manner.
"""
import datetime
import logging
import voeparse
import pysovo
from pysovo.local import contacts
from pysovo.formatting import datetime_format_short



def main():
    now = datetime.datetime.utcnow()
    test_packet = voeparse.Voevent(stream='voevent.astro.soton/TEST',
                                   stream_id=now.strftime(datetime_format_short),
                                   role=voeparse.roles.test)
    print "Sending packet, ivorn: ", test_packet.attrib['ivorn']
    broker = contacts['vobroker']
    before = datetime.datetime.utcnow()
    pysovo.comms.comet.send_voevent(test_packet, broker['host'], broker['port'])
    after = datetime.datetime.utcnow()
    print "Done. Sending took", (after - before).total_seconds(), "seconds."

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
