"""
Commonly used routines for determining target ephemeris and visibilities.
"""
from __future__ import absolute_import
import ephem
import math
import pytz
from collections import OrderedDict
DEG_PER_RADIAN = 180 / math.pi


# -----------------------------------------------------------------
class TargetStatusKeys():
    """A namespaced set of dict keys for visibility reports"""
    site_lst = 'site_lst'
    type = 'type'
    visible_now = 'visible_now'
    current_pos = 'current_position'
    prev_transit_time = 'prev_transit_time'
    prev_transit_pos = 'prev_transit_position'
    next_transit_time = 'next_transit_time'
    next_transit_pos = 'next_transit_position'
    rise_time = 'rise_time'
    set_time = 'set_time'
    timeline = 'timeline'


def get_ephem(eq_posn, observer, current_time):
    """Get basic information on target visibility for a given site.

    Returns a dict populated with relevant TargetStatusKeys.
    """
    keys = TargetStatusKeys
    assert isinstance(observer, ephem.Observer)
    # Get times:

    observer.date = current_time
    fixedbody = ephem.FixedBody()
    fixedbody._ra = eq_posn.ra
    fixedbody._dec = eq_posn.dec
    fixedbody._epoch = eq_posn.epoch
    fixedbody.compute(observer)

    result = {}
    result[keys.site_lst] = str(observer.sidereal_time())
    result[keys.current_pos] = (fixedbody.alt * DEG_PER_RADIAN,
                                fixedbody.az * DEG_PER_RADIAN)
    result[keys.visible_now] = (fixedbody.alt > observer.horizon)

    if fixedbody.neverup:
        result[keys.type] = 'never'
        return result

    result[keys.next_transit_time] = pytz.utc.localize(
        observer.next_transit(fixedbody).datetime())
    result[keys.prev_transit_time] = pytz.utc.localize(
        observer.previous_transit(fixedbody).datetime())

    if fixedbody.circumpolar:
        # Circumpolar
        result[keys.type] = 'always'
        events = ['previous_transit','next_transit' ]
    else:
        # Regular rise and set
        result[keys.type] = 'sometimes'
        events = [
            'previous_rising', 'previous_transit', 'previous_setting',
            'next_rising', 'next_transit', 'next_setting',
        ]
    # Returns timezone unaware ('naive') datetimes
    timeline = {}
    for event_name in events:
        observer_func =  getattr(observer, event_name)
        event_date = pytz.utc.localize(observer_func(fixedbody).datetime())
        timeline[event_date] = event_name.replace('_',' ').capitalize()
    timeline[current_time] = '(Trigger received)'

    result[keys.timeline]=OrderedDict()
    for dtime in sorted(timeline):
        result[keys.timeline][dtime] = timeline[dtime]

    transit_observer = ephem.Observer()
    transit_observer.lon = observer.lon
    transit_observer.lat = observer.lat
    transit_observer.horizon = observer.horizon
    transit_observer.date = result[keys.next_transit_time]
    fixedbody.compute(transit_observer)
    result[keys.next_transit_pos] = (fixedbody.alt * DEG_PER_RADIAN,
                              fixedbody.az * DEG_PER_RADIAN)

    return result
