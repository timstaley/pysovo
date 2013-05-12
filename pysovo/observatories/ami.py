from astropysics.coords.coordsys import FK5Coordinates
from astropysics.obstools import Site

import datetime
#import jinja2
from jinja2 import Environment, PackageLoader

from pysovo import comms

env = Environment(loader=PackageLoader('pysovo', 'templates'),
                  trim_blocks=True)

#Handy values:
default_action = 'QUEUE'
request_email_subject = 'AMI Request'
##---------------------------------------------------------------
## astropysics.obstools.Site details:
site = Site(lat='+52:12:29',
          long='+0:7:21',
          alt=15,
          tz=0,
          name='AMI'
          )
site.target_min_elevation = 20
site.long_name = 'Arcminute Microkelvin Imager, MRAO',

##---------------------------------------------------------------
def request_observation(target_coords,
                        target_name,
                        duration,
                        timing,
                        requested_action,
                        requester,
                        recipient_email_address,
                        email_account,
                        comment='Uncommented pysovo request',
                        ):
    """Simply combines email formatting and sending, to trigger an email request."""

    mail_text = _typeset_obs_request_email(
                       target_coords, target_name,
                       timing,
                       action=requested_action,
                       requester=requester,
                       duration=duration,
                       comment=comment,
                       array='AMI-LA')
#    print "Mail text:"
#    print mail_text
    comms.email.send_email(email_account,
                           recipient_addresses=recipient_email_address,
                           subject=request_email_subject,
                           body_text=mail_text)
    return mail_text
##---------------------------------------------------------------

#Formatting specification, for reference:
"""
  Array=     AMI-SA
  Target=    GRB110328A
  J2000RA=   16 44 49.93
  J2000Dec=  57 35 59.1
  Timing=    ST 15.45
  Duration=  02.00
  Requester= djt
  Comment=   Target of Opportunity test

where:

 'Array'     must be either 'AMI-SA' or 'AMI-LA'.
 'Target' and the J2000 coordinates define the observation target.
 'Timing'    specifies the start of the observation, either by Local
             Sidereal Time 'ST hh.mm', or by using one of the keywords
             'Transit' (to observe through transit) or 'ASAP' (to start
             the observation as soon as possible).
 'Duration'  specifies the length of the observation (hh.mm).
 'Requester' identifies the observer.
 'Comment'   adds a string of comment text to the observation header.
"""


#def format_ami_coords(coords):
#    """Converts astropysics FK5 coords to AMI formatted ra,dec strings."""
#
#    ra_str = coords.ra.getHmsStr(canonical=True).replace(':', ' ')
#    dec_str = coords.dec.getDmsStr(canonical=True).replace(':', ' ')
#    if coords.dec.degrees >= 0:
#        #Drop the '+' symbol
#        dec_str = dec_str[1:]
#    return ra_str, dec_str

def _format_fk5_to_ami_ra(coords):
    """Converts astropysics FK5 coords to AMI formatted ra string."""
    return  coords.ra.getHmsStr(canonical=True).replace(':', ' ')

def _format_fk5_to_ami_dec(coords):
    """Converts astropysics FK5 coords to AMI formatted dec string."""
    dec_str = coords.dec.getDmsStr(canonical=True).replace(':', ' ')
    if coords.dec.degrees >= 0:
        #Drop the '+' symbol
        dec_str = dec_str[1:]
    return dec_str


def _format_timedelta_to_ami_duration(duration):
    """Format duration string in AMI compliant format.

    Rounds down to nearest minute.
    """
    assert isinstance(duration, datetime.timedelta)
    hrs = duration.seconds // 3600
    minutes = (duration.seconds - hrs * 3600) // 60
    return '.'.join((str(hrs).zfill(2), str(minutes).zfill(2)))

env.filters['ami_ra'] = _format_fk5_to_ami_ra
env.filters['ami_dec'] = _format_fk5_to_ami_dec
env.filters['ami_duration'] = _format_timedelta_to_ami_duration

ami_alert_template = env.get_template('ami_alert_template.txt')

def _typeset_obs_request_email(
                    target_coords,
                    target_name,
                    timing,
                    duration,
                    action,
                    requester,
                    comment,
                    array
                    ):
    """
    Validates the tightly constrained fields,
    and enforces formatting via template filters.

    *Args*
    - target_coords: Should be astropysics.coordinates.coordsys.FK5Coordinates

    - target_name: String, up to 16 chars (any overrun will be dropped)

    - timing: String specifying when to observe, one of  ['ASAP', 'Transit', 'ST']
        i.e.:  -as soon as possible, when transiting, or at a specified
        sidereal time (last option not currently supported).

    - action:  Either 'QUEUE' (queue the request) or any of 3 synonyms,
            ['CHECK', 'VERIFY', 'QUERY'], which will result in a reply email
            detailing request validity and observing conditions,
            but will not actually queue the observation.

    - requester: The requester's identity.

    - duration: datetime.timedelta - requested observation length
        (sensibly this should be anywhere from 30 minutes to a few hours).

    - comment: String, up to 256 chars (any overrun will be dropped)

    - Array: String, One of ['AMI-LA', 'AMI-SA'].

    *Returns*:
    String, formatted email body.
    """
    if array not in ['AMI-LA', 'AMI-SA']:
        raise ValueError('Invalid AMI array choice')

    if timing not in ['ASAP', 'Transit']:
        if timing.find('ST') != 0:
            raise ValueError('Invalid AMI timing choice')

    if action not in ['QUERY', 'CHECK', 'VERIFY', 'QUEUE']:
        raise ValueError('Invalid AMI action choice')

    assert isinstance(target_coords, FK5Coordinates)
    return ami_alert_template.render(**locals())


