#!/usr/bin/python
import sys, os
import datetime, pytz
from pysovo import observatories as obs
import pysovo as ps

#-----------------------------------------------------------------------------------------
notify_contacts = []
notify_contacts.extend([ps.address_book.tim,
                         ps.address_book.rob,
                         ps.address_book.rene, ])

notification_email_subject = "4 Pi Sky notification"

default_archive_root = os.environ["HOME"] + "/comet/voe_archive"

local_config = ps.LocalConfig(email_account=ps.email.load_account_settings_from_file(),
                              sms_account=ps.sms.load_account_settings_from_file())


#-----------------------------------------------------------------------------------------
def main():
    s = sys.stdin.read()
    v = ps.voevent.build.from_string(s)
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
    posn = ps.voevent.pull_astro_coords(v)
    if posn.dec.degrees > -10.0:
        obs.ami.request_observation(posn,
                                    ps.alert_types.swift_grb,
                                    v,
                                    local_config)

        long_msg, short_msg = ps.notifications.obs_requested_message(posn,
                                      event_time=now, #should grab from voevent
                                      description="SWIFT GRB",
                                      obs_site=obs.ami,
                                      current_time=now)

    else:
        long_msg, short_msg = ps.notifications.event_missed_message(posn,
                                      event_time=now, #should grab from voevent
                                      description="SWIFT GRB",
                                      reason_missed="No suitable observation facilities")

    ps.notifications.notify(local_config,
                            notify_contacts,
                            subject=notification_email_subject + ": Swift GRB",
                            long_message=long_msg,
                            send_sms=False,
                            short_message=short_msg)

def test_logic(v):
    now = datetime.datetime.now(pytz.utc)
    msg = "Test packet receieved at time " + now.strftime("%y-%m-%d_%H-%M-%S") + "\n"
    ps.notifications.notify(ps.address_book.tim,
                            msg)

def archive_voevent(v, rootdir):
    relpath, filename = v.attrib['ivorn'].split('//')[1].split('#')
    filename += ".xml"
    fullpath = os.path.sep.join((rootdir, relpath, filename))
    ps.utils.ensure_dir(fullpath)
    with open(fullpath, 'w') as f:
        f.write(ps.voevent.output.to_string(v))


if __name__ == '__main__':
    sys.exit(main())

