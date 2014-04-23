from __future__ import absolute_import

import voeparse as vp
import datetime
from copy import copy
import pysovo.utils


def create_skeleton_4pisky_voevent(substream, stream_id,
                                   role=vp.definitions.roles.test):
    v = vp.Voevent(stream='voevent.phys.soton.ac.uk/' + substream,
               stream_id=stream_id, role=role)
    vp.set_who(v, date=datetime.datetime.utcnow(),
               author_ivorn=None)
    vp.set_author(v,
                  shortName="4PiSky",
                  contactName="Tim Staley",
                  contactEmail="tim.staley@astro.ox.ac.uk"
                  )
    return v

def create_ami_followup_notification(alert, stream_id,
                                request_status,
                                superseded_ivorns=None):

    orig_pkt = alert.voevent
    voevent = create_skeleton_4pisky_voevent('AMI-REQUEST', stream_id,
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
    g = vp.Group(request_params, name='ami-request')
    voevent.What.append(g)
    
    # Also copy target location into WhereWhen
    voevent.WhereWhen = copy(orig_pkt.WhereWhen)
    # But the time marker should refer to the AMI observation:
    # (We are already citing the original Swift alert)
    ac = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords
    del ac.Time
    voevent.WhereWhen.Description = "Target co-ords from original Swift BAT alert"

    return voevent
    



