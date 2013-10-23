from __future__ import absolute_import

import voeparse as vp
import datetime
from copy import copy
import pysovo.utils


def create_skeleton_4pisky_voevent(substream, stream_id, role=vp.roles.test):
    v = vp.Voevent(stream='voevent.phys.soton.ac.uk/' + substream,
               stream_id=stream_id, role=role)
    vp.set_who(v, date=datetime.datetime.now(),
               author_ivorn=None)
    vp.set_author(v, title="4PiSky",
                  shortName="4PiSky",
                  contactName="Tim Staley"
                  )
    return v

def create_ami_followup_notification(original_alert_voevent, stream_id,
                                request_status,
                                superseded_ivorns=None):

    orig = original_alert_voevent
    note = create_skeleton_4pisky_voevent('AMI-REQUEST',
                                       stream_id, role=vp.roles.utility)
    vp.add_how(note, descriptions="AMI Large Array, Cambridge",
               references=vp.Reference("http://www.mrao.cam.ac.uk/facilities/ami/ami-technical-information/"),
               )
    note.Why = copy(orig.Why)
    vp.add_citations(note, citations=vp.Citation(ivorn=orig.attrib['ivorn'],
                              cite_type=vp.definitions.cite_types.followup))
    note.What.Description = "A request for AMI-LA follow-up has been made."
    
    request_params = [vp.Param(key, val)
                      for key, val in request_status.iteritems()]
    g = vp.Group(request_params, name='request')
    note.What.append(g)
    
    coords = vp.pull_astro_coords(orig)
    target_posn = pysovo.utils.namedtuple_to_dict(coords)
    target_pars = [vp.Param(key, val)
                      for key, val in target_posn.iteritems()]
    g = vp.Group(target_pars, name='target')
    note.What.append(g)

    return note
    



