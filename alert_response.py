#!/usr/bin/python
import sys, os
import datetime, pytz
import voeparse
import logging
logging.basicConfig(level=logging.DEBUG)

from pysovo import contacts
from pysovo.formatting import format_datetime
import pysovo as ps
import ami

from jinja2 import Environment, PackageLoader

#-------------------------------------------------------------------------------
notify_contacts = [contacts['tim'],
                   contacts['rob'],
                   contacts['rene'], ]

notification_email_prefix = "[4 Pi Sky] "

default_archive_root = os.environ["HOME"] + "/comet/voe_archive"

active_sites = [ami.site]


env = Environment(loader=PackageLoader('pysovo', 'templates'),
                  trim_blocks=True)
env.filters['datetime'] = format_datetime

#-------------------------------------------------------------------------------
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

        ami_request = ami.request_email(posn, target_name, duration,
                      timing='ASAP',
                      action='QUEUE',
                      requester=contacts['ami']['requester'],
                      comment=comment)
        ps.comms.email.send_email(account=ps.default_email_account,
                                recipient_addresses=contacts['ami']['email'],
                                subject=ami.request_email_subject,
                                body_text=ami_request)

        actions_taken.append('Observation requested from AMI.')

    notify_msg = generate_report_text(
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

def generate_report_text(target_info, sites, dtime, actions_taken):
    posn = target_info['position']
    site_reports = [(site, ps.ephem.visibility(posn, site, dtime))
                            for site in sites]
    notification_template = env.get_template('notify_example.txt')
    msg = notification_template.render(target=target_info,
                                note_time=dtime,
                                site_reports=site_reports,
                                actions_taken=actions_taken,
                                dt_style=ps.formatting.datetime_format_long)
    return msg

if __name__ == '__main__':
    sys.exit(main())

