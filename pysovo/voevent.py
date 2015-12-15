from __future__ import absolute_import

import voeventparse as vp
import datetime
from copy import copy


ivorn_base = 'voevent.4pisky.org'
test_trigger_substream = 'TEST-TRIGGER'
test_response_substream = 'TEST-RESPONSE'
alarrm_request_substream = 'ALARRM-REQUEST'
datetime_format_short = '%y%m%d-%H%M.%S'

def create_skeleton_4pisky_voevent(substream, stream_id,
                                   role=vp.definitions.roles.test,
                                   date=None):
    author_ivorn = ivorn_base+'/robots'
    if date is None:
        date = datetime.datetime.utcnow()

    v = vp.Voevent(stream=ivorn_base+ '/' + substream,
               stream_id=stream_id, role=role)

    vp.set_who(v, date=date,
               author_ivorn=author_ivorn)
    vp.set_author(v,
                  shortName="4PiSkyBot",
                  contactName="Tim Staley",
                  contactEmail="tim.staley@physics.ox.ac.uk"
                  )
    return v

def create_4pisky_test_trigger_voevent():
    now = datetime.datetime.utcnow()
    test_packet = create_skeleton_4pisky_voevent(
        substream=test_trigger_substream,
        stream_id=now.strftime(datetime_format_short),
        role=vp.definitions.roles.test,
        date=now,
    )
    return test_packet

def create_4pisky_test_response_voevent(stream_id, date):
    response = create_skeleton_4pisky_voevent(
        substream=test_response_substream,
        stream_id=stream_id,
        role=vp.definitions.roles.test,
        date=date
    )
    return response

def create_ami_followup_notification(alert, stream_id,
                                request_status,
                                superseded_ivorns=None):

    orig_pkt = alert.voevent
    voevent = create_skeleton_4pisky_voevent(
        substream=alarrm_request_substream,
        stream_id=stream_id,
        role=vp.definitions.roles.utility)
    vp.add_how(voevent, descriptions="AMI Large Array, Cambridge",
               references=vp.Reference(
                   "http://www.mrao.cam.ac.uk/facilities/ami/ami-technical-information/"),
    )
    voevent.Why = copy(orig_pkt.Why)
    vp.add_citations(voevent, citations=vp.Citation(ivorn=orig_pkt.attrib['ivorn'],
                              cite_type=vp.definitions.cite_types.followup))
    voevent.What.Description = "A request for AMI-LA follow-up has been made."
    
    request_params = [vp.Param(key, val)
                      for key, val in request_status.iteritems()]
    g = vp.Group(request_params, name='request_status')
    voevent.What.append(g)
    
    # Also copy target location into WhereWhen
    voevent.WhereWhen = copy(orig_pkt.WhereWhen)
    # But the time marker should refer to the AMI observation:
    # (We are already citing the original Swift alert)
    ac = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords
    del ac.Time
    voevent.WhereWhen.Description = "Target co-ords from original Swift BAT alert"

    return voevent
    



