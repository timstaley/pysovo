#pysovo VOEvent Tools
#Convenience functions allowing easy access to information in VOEvent packets. 
#Tim Staley, <timstaley337@gmail.com>, 2012

from lxml import objectify
from astropysics.coords.coordsys import FK5Coordinates

class build(object):
    @staticmethod
    def from_string(s):
        """
        Wrapper to parse a VOEvent tree, taking care of some subtleties.
        
        Currently pretty basic, but we can imagine using this function to 
        homogenise or at least identify different VOEvent versions, etc.
        
        NB The namespace is removed from the root element tag to make 
        objectify access work as expected, so we must re-add it with 
        <output function to be determined> when we want to conform to schema.  
        """
        v = objectify.fromstring(s)
        build._remove_root_tag_prefix(v)
        return v

    @staticmethod
    def from_file(path):
        s = open(path, 'rb').read()
        return build.from_string(s)

    @staticmethod
    def _remove_root_tag_prefix(v):
        """
        Removes 'voe' namespace prefix from root tag.
        
        When we load in a VOEvent, the root element has a tag prefixed by
         the VOE namespace, e.g. {http://www.ivoa.net/xml/VOEvent/v2.0}VOEvent
        Because objectify expects child elements to have the same namespace as 
        their parent, this breaks the python-attribute style access mechanism.
        We can get around it without altering root, via e.g
         who = v['{}Who']
        But I prefer this solution: 
        by simply replacing the namespace tag with an empty entry,
        everything works as expected.
        (Until the time comes to write out the VOEvent! So take care.) 
        """
        v.tag = v.tag.replace(v.nsmap['voe'], '')
        return
#
#def get_param_names(v):
#    '''
#    Grabs the "what" section of a voevent, and produces a list of tuples of group name and param name.
#    For a bare param, the group name is the empty string.
#    
#    NB. This replicates functionality from VOEventLib - but the inbuilt version is broken as of v0.3.
#    '''
#    list = []
#    w = v.What
#    if not w: return list
#    for p in v.What.Param:
#        list.append(('', p.name))
#    for g in v.What.Group:
#        for p in g.Param:
#            list.append((g.name, p.name))
#    return list
#

class CoordSystemIDs(object):
    fk5 = 'UTC-FK5-GEO'

def pull_astro_coords(v):
    """Attempts to determine coords system and convert to corresponding
       astropysics class.
    """
    ac = v.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords
    ac_sys = v.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoordSystem

    if ac_sys.attrib['id'] != CoordSystemIDs.fk5:
        raise ValueError("Cannot extract astro_coords, unrecognised coord system")

    try:
        assert ac.Position2D.Name1 == 'RA'
        ra_deg = ac.Position2D.Value2.C1
        dec_deg = ac.Position2D.Value2.C2
        err_deg = ac.Position2D.Error2Radius
    except AttributeError:
        raise ValueError("Unrecognised AstroCoords type")
    return FK5Coordinates(ra=ra_deg, dec=dec_deg,
                          raerror=err_deg, decerror=err_deg)


#
#def get_isotime(v):
#    assert isinstance(v, voe.VOEvent)
#    try:
#        ol = v.WhereWhen.ObsDataLocation.ObservationLocation
#        return ol.AstroCoords.Time.TimeInstant.ISOTime
#    except:
#        return None
#
#def make_Who(names, emails):
#    names = listify(names)
#    emails = listify(emails)
#    w = voe.Who()
#    w.Author = voe.Author()
#    w.Author.contactName = names
#    w.Author.contactEmail = emails
#    return w
