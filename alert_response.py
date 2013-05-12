#!/usr/bin/python
import sys, os
import datetime, pytz
import voeparse
import logging
logging.basicConfig(level=logging.DEBUG)

from pysovo import observatories as obs
from pysovo import contacts
import pysovo as ps

#-----------------------------------------------------------------------------------------
notify_contacts = [contacts['tim'],
                   contacts['rob'],
                   contacts['rene'], ]

notification_email_prefix = "[4 Pi Sky] "

default_archive_root = os.environ["HOME"] + "/comet/voe_archive"

active_sites = [obs.ami.site]

#-----------------------------------------------------------------------------------------
def main():
    s = sys.stdin.read()
    v = voeparse.loads(s)
    voevent_logic(v)
    return 0

def voevent_logic(v):
    #SWIFT BAT GRB alert:
    if v.attrib['ivorn'].find("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos") == 0:
        swift_bat_grb_logic(v)

    if v.attrib['ivorn'].find("ivo://voevent.astro.soton/TEST#") == 0:
        test_logic(v)
    archive_voevent(v, rootdir=default_archive_root)



def swift_bat_grb_logic(v):
    now = datetime.datetime.now(pytz.utc)
    posn = ps.utils.convert_voe_coords_to_fk5(voeparse.pull_astro_coords(v))
    actions_taken = []
    alert_id, alert_id_short = ps.utils.pull_swift_bat_id(v)
    target_name = 'SWIFT_' + alert_id_short
    comment = 'Automated SWIFT ID ' + alert_id

    if posn.dec.degrees > -10.0:
        duration = datetime.timedelta(hours=1)

        obs.ami.request_observation(posn, target_name, duration,
                        timing='ASAP',
                        requested_action='QUEUE',
                        requester=contacts['ami']['requester'],
                        recipient_email_address=contacts['ami']['email'],
                        email_account=ps.default_email_account,
                        comment=comment,
                        )
        actions_taken.append('Observation requested from AMI.')

    notify_msg = ps.notify.generate_report_text(
                                {'position': posn, 'description': 'Swift GRB'},
                                active_sites,
                                now,
                                actions_taken)
    ps.comms.email.send_email(ps.default_email_account,
                        [p['email'] for p in notify_contacts],
                        notification_email_prefix + target_name,
                        notify_msg)



def test_logic(v):
    now = datetime.datetime.now(pytz.utc)
    msg = "Test packet received at time %s\n" % now.strftime("%y-%m-%d %H:%M:%S")
    ps.comms.email.send_email(ps.default_email_account,
                            contacts['test']['email'],
                            'Test packet received',
                            msg)
    archive_voevent(v, rootdir=default_archive_root)

def archive_voevent(v, rootdir):
    relpath, filename = v.attrib['ivorn'].split('//')[1].split('#')
    filename += ".xml"
    fullpath = os.path.sep.join((rootdir, relpath, filename))
    ps.utils.ensure_dir(fullpath)
    with open(fullpath, 'w') as f:
        voeparse.dump(v, f)


if __name__ == '__main__':
    sys.exit(main())

