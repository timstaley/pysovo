#!/usr/bin/python


#Minimal imports here - ensures proper testing of alert_response.
#(If not careful you might temporarily fix a broken import - which then remains broken)
from pysovo.tests.resources import datapaths
from pysovo.formatting import datetime_format_short
import voeparse
import alert_response as ar
import datetime

##We bind the email sender to a dummy function:
ar.ps.comms.email.send_email = ar.ps.comms.email.dummy_email_send_function
ar.ps.comms.comet.send_voevent = ar.ps.comms.comet.dummy_send_to_comet_stub

def main():
    ar.default_archive_root = "./"
    now = datetime.datetime.utcnow()
    test_packet = voeparse.Voevent(stream='voevent.astro.soton/TEST',
                                   stream_id=now.strftime(datetime_format_short),
                                   role=voeparse.roles.test)
    print "Packet loaded, ivorn", test_packet.attrib['ivorn']
    ar.voevent_logic(test_packet)

if __name__ == "__main__":
    main()
