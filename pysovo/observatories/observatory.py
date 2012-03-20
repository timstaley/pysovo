import astropysics.obstools
from astropysics.coords.coordsys import FK5Coordinates 

import datetime
import pytz


class Observatory(astropysics.obstools.Site):
    """Extends astropysics.obstools.site.
    
    Additional features: 
        * Check if target is on-sky.
        * Get next rise / set /transit times.
        * Check if observatory open for ToOs.
        * Provide observation request methods.
    
    See also:
    http://packages.python.org/Astropysics/coremods/obstools.html#astropysics.obstools.Site
    
    """
    def __init__(self,
                 lat, long,
                 site_altitude=0,
                 target_min_elevation=0,
                 tz=None,
                 name=None,
                 short_name=None,
                 email_address=None,
                 ip_address=None
                 ):
        
        astropysics.obstools.Site.__init__(self, 
                                           lat, long, 
                                           site_altitude, 
                                           tz, 
                                           name)
        self.short_name = short_name
        self.email_address = email_address
        self.ip_address = ip_address
        self.target_min_elevation = target_min_elevation #Minimum target elevation, in degrees above horizon
    
    @staticmethod
    def check_available():
        """A function to determine whether an observatory is currently available for ToO requests.
        
        Where possible, this should either communicate with the observatory directly,
        or perhaps check a local table of availability to be updated as necessary.
        
        """
        raise NotImplementedError
        
    @staticmethod
    def request_observation(coords, 
                            alert_type, 
                            voevent, 
                            local_config, 
                            **kwargs):
        """ Implemented and assigned on a per-observatory basis. 
            (Still thinking about common parameters)
            TODO: Think about best way to implement an "observation length" argument
        """
        raise NotImplementedError
    
    @staticmethod
    def internal_request_mechanism(request_info, local_config, **kwargs):
        """ I am specifying as part of the interface that this should be encapsulated,  
            Then called as part of the `request_observation` function.
            
            This allows for easy testing as the message content can then easily be redirected.
            The real-world mechanism (e.g. email, voevent) can then be tested separately.
            
            For interoperability it is recommended that internal_request_mechanism
            calls are made with all arguments specified by keywords.
        """
        raise NotImplementedError
    
    
    def riseSetTransit_datetimes(self, eqpos, date, alt=0):
        """Gets the transit time for the given date, and the rise/set either side
        
        This is actually a wrapper to the astropysics functionality, 
        which returned a time (but no date!) when I first started testing.
        However, I believe this has now been fixed. 
            
        TO DO: Check current astropysics functionality and remove this wrapper if appropriate.
        """ 
        #Transit corresponds to specified date:
        
        r, s, t = self.riseSetTransit(eqpos, date, alt, timeobj=True, utc=True)
        if t is not None:
            transit = datetime.datetime.combine(date, t)
        else:
            transit = None
#        transit =  combine_date_time(date, t) 
        #Need to avoid comparisons against NoneType in circumpolar / below horizon case
        if r is None:
            return (r, s, transit)
        
        if r<t:
            rise  = datetime.datetime.combine(date, r)
        else:
            rise = datetime.datetime.combine(date - datetime.timedelta(1), r)
            
        if s>t:
            set  = datetime.datetime.combine(date, s)
        else:
            set = datetime.datetime.combine(date + datetime.timedelta(1), s)
            
        return ( rise, set, transit )
    
    def on_sky(self, eqpos, specific_time):
        """Checks if a target is on sky at the specified datetime.
        
        Note: Uses the minimum_elevation attribute of the observatory, if not None.
        
        TO DO: Backport functionality to astropysics.
        
        """
#        if specific_time==None:
#            t = datetime.datetime.now(pytz.utc)
#        else:
        t = specific_time
        if self.target_min_elevation is not None:
            min_elevation = self.target_min_elevation
        else:
            min_elevation = 0
                    
        rise,set,transit = self.riseSetTransit_datetimes(eqpos, t.date(), min_elevation)
        
        tomorrow = t.date()+datetime.timedelta(1)
        #NB although today's transit may have set, tomorrow's transit may rise before midnight... 
        rise_before_tomorrows_transit = self.riseSetTransit_datetimes(eqpos, tomorrow, min_elevation)[0]
        
        if transit is not None and rise is None: #Circumpolar case
            return True
        elif transit is None:  #Always below horizon case
            return False
        elif rise <= t <= set: #Within today's transit
            return True
        elif rise_before_tomorrows_transit is not None: #Last possible chance for on-sky
            return rise_before_tomorrows_transit < t
        else:
            return False #Does this case ever occur? 
            #I think maybe if today is the last day before precession knocks it out of visibility.  
    
    def next_riseSetTransit(self, eqpos, specific_time, alt=0):
        """Get 'next' r,s,t for a target at a given UTC datetime (see details).
        
        If on-sky at the specified datetime, returns the rise / set times bracketing current transit,
        (so rise and possibly transit will be in the past at specified time).
        Otherwise rise/transit/set will all be in the future.
            
        If circumpolar (always visible) rise/set are None, but transit is specified.
        If never visible, rise / set / transit are all None.
        
        NB The only dates checked for visibility are 'today' and 'tomorrow'
        (relative to given datetime). 
        If the target is an edge case that's below the horizon all day today,
        but is visible in 6 months, you will still get a None result.
        
        TO DO: Backport to astropysics.
        
        """
#        if specific_time==None:
#            t = datetime.datetime.now(pytz.utc)
#        else:
        t = specific_time
            
        tomorrow = t.date()+datetime.timedelta(1)
        
        #Today's transit
        rise0,set0,transit0 = self.riseSetTransit_datetimes(eqpos, t.date(), alt)
        #Tomorrow's transit (may rise before midnight today) 
        rise1,set1,transit1 = self.riseSetTransit_datetimes(eqpos, tomorrow, alt)
        
        if transit0 is not None and rise0 is None: #Circumpolar case, have we passed today's transit?
            if t < transit0:
                return (rise0,set0,transit0) #i.e. (None,None,t0)
            else:
                return (rise1,set1,transit1) #i.e. (None,None,t1)
        elif transit0 is None:  #Always below horizon case
            return (rise0,set0,transit0)  #(None,None,None)
        elif rise0 <= t <= set0: #Within today's transit (can perform comparison, since we checked already if r0 is None)
            return (rise0,set0,transit0)
        else: #Possibly on sky if rise1 has passed already. 
            return (rise1,set1,transit1) #Valid either way as transit1 must be tomorrow (i.e., future)
        
