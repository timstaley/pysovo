#pysovo VOEvent Tools
#Copyright Tim Staley, <timstaley337@gmail.com>, 2012

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
        
        Returns a boolean.
        """
        raise NotImplementedError
        return False

    @staticmethod
    def request_observation(coords,
                            alert_type,
                            voevent,
                            local_config,
                            **kwargs):
        """ Implemented and assigned on a per-observatory basis. 
            (Still thinking about common parameters)
            TODO: Think about best way to implement an "observation length" argument
            
            Returns a dictionary.
        """
        raise NotImplementedError
        return dict()

    @staticmethod
    def internal_request_mechanism(request_info, local_config, **kwargs):
        """ 
        I am specifying as part of the interface that this should be 
        encapsulated as a function,  
        then called as part of the `request_observation` function.
        
        This allows for easy testing -
        by monkey-patching in a different request function,
        the message content can easily be redirected so as not to trigger a 
        false alarm.
        The real-world mechanism (e.g. email, voevent) can then be tested separately.
        
        For interoperability it is recommended that internal_request_mechanism
        calls are made with all arguments specified by keywords.
        """
        raise NotImplementedError
