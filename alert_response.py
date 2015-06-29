#!/usr/bin/env python
import sys, os
import datetime, pytz
import voeventparse
import logging
import subprocess
import socket
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from pysovo.local import contacts
from pysovo.visibility import get_ephem
from pysovo.triggers import swift
import pysovo as ps
import amiobs

from jinja2 import Environment, PackageLoader

#-------------------------------------------------------------------------------
grb_contacts = contacts.grb_contacts


notification_email_prefix = "[4 Pi Sky] "

default_archive_root = os.path.join(os.environ["HOME"],
                                    "voevent-deploy","voe_archive")

active_sites = [amiobs.site]

env = Environment(loader=PackageLoader('pysovo', 'templates'),
                  trim_blocks=True,lstrip_blocks=True)
env.filters['datetime'] = ps.formatting.format_datetime
env.filters['rad_to_deg'] = ps.formatting.rad_to_deg

#-------------------------------------------------------------------------------

def main():
    s = sys.stdin.read()
    v = voeventparse.loads(s)
    voevent_logic(v)
    return 0

def voevent_logic(v):
    #SWIFT BAT GRB alert:
    if swift.filters.is_bat_grb_pkt(v):
        swift_bat_grb_logic(v)
    if v.attrib['ivorn'].find("ivo://voevent.astro.soton/TEST#") == 0:
        test_logic(v)
    archive_voevent(v, rootdir=default_archive_root)


def swift_bat_grb_logic(v):
    actions_taken=[]
    alert = swift.BatGrb(v)
    alert_rejection = alert.reject()
    if alert_rejection is None:
        ami_reject = ps.filters.ami.reject(alert.position)
        if ami_reject is None:
            try:
                trigger_ami_swift_grb_alert(alert)
                actions_taken.append('Observation requested from AMI.')
                try:
                    send_initial_ami_alert_vo_notification(alert)
                    actions_taken.append('AMI request notified to VOEvent network.')
                except subprocess.CalledProcessError as e:
                    emsg = '***Notification to VOEvent network failed.***'
                    logger.warn(emsg)
                    actions_taken.append(emsg)
            except Exception as e:
                emsg = 'Observation request failed.'
                actions_taken.append(emsg)
                logger.error(emsg)
                raise
        else:
            actions_taken.append('Target rejected by ami: ' + ami_reject)
    else:
        actions_taken.append('Alert ignored: ' + alert_rejection)

    send_alert_report(alert, actions_taken, grb_contacts)




def trigger_ami_swift_grb_alert(alert):
    assert isinstance(alert, swift.BatGrb)
    target_name = alert.id
    comment = alert.id + " / " + alert.inferred_name
    duration = datetime.timedelta(hours=2.)

    ami_request = amiobs.request_email(
                   target_coords=alert.position,
                   target_name=target_name,
                   duration=duration,
                  timing='ASAP',
                  action='QUEUE',
                  requester=amiobs.default_requester,
                  comment=comment)

    ps.comms.email.send_email(recipient_addresses=amiobs.email_address,
                              subject=amiobs.request_email_subject,
                              body_text=ami_request)





def send_initial_ami_alert_vo_notification(alert):
    notification_timestamp = datetime.datetime.utcnow()
    request_status = {'sent_time':notification_timestamp,
                  'acknowledged':False,
                  }
    stream_id = notification_timestamp.strftime(ps.formatting.datetime_format_short)
    v = ps.voevent.create_ami_followup_notification(alert,
                                             stream_id=stream_id,
                                             request_status=request_status)
    ps.comms.comet.send_voevent(v, contacts.local_vobroker.ipaddress,
                                contacts.local_vobroker.port)


def send_alert_report(alert, actions_taken, contacts):
    notify_msg = generate_report_text(
                                alert,
                                active_sites,
                                actions_taken)
    subject = alert.id
    if alert.inferred_name is not None:
              subject+= ' / ' + alert.inferred_name
    ps.comms.email.send_email([p.email for p in contacts],
                              notification_email_prefix + subject,
                              notify_msg)


def test_logic(v):
    now = datetime.datetime.now(pytz.utc)
    msg = "Test packet received at time %s\n" % now.strftime("%y-%m-%d %H:%M:%S")
    stream_id = v.attrib['ivorn'].partition('#')[-1]
    response = voeventparse.Voevent(stream='voevent.astro.soton/TESTRESPONSE',
                                   stream_id=stream_id,
                                   role=voeventparse.definitions.roles.test)
    ps.comms.comet.send_voevent(response, contacts.local_vobroker.ipaddress,
                                contacts.local_vobroker.port)

    ps.comms.email.send_email(
        recipient_addresses=[c.email for c in contacts.test_contacts],
        subject='[VO-TEST] Test packet received',
        body_text=msg)
    archive_voevent(v, rootdir=default_archive_root)


def archive_voevent(v, rootdir):
    relpath, filename = v.attrib['ivorn'].split('//')[1].split('#')
    filename += ".xml"
    fullpath = os.path.sep.join((rootdir, relpath, filename))
    ps.utils.ensure_dir(fullpath)
    with open(fullpath, 'w') as f:
        voeventparse.dump(v, f)

def generate_report_text(alert, sites, actions_taken,
                         report_timestamp=None):
    if report_timestamp is None:
        report_timestamp = datetime.datetime.now(pytz.utc)
    site_reports = [(site, get_ephem(alert.position, site, report_timestamp))
                            for site in sites]
    hostname = socket.gethostname()
    notification_template = env.get_template('notify.txt')
    msg = notification_template.render(alert=alert,
                                report_timestamp=report_timestamp,
                                site_reports=site_reports,
                                actions_taken=actions_taken,
                                dt_style=ps.formatting.datetime_format_long,
                                hostname=hostname
                                )
    return msg

if __name__ == '__main__':
    sys.exit(main())

