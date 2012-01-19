import sys
import voe as voevent

#class dkeys:
#    """Convenience class.
#    Allows easy autocompletion for the dictionary key strings
#    used in the utils module,
#    when using PyDev IDE"""
#    isotime="isotime"

class VOEventExportClass(voevent.VOEvent):
    def __init__(self, event, schemaURL):
        self.event = event
        self.schemaURL = schemaURL

    def export(self, outfile, level, namespace_='', name_='voevent', namespacedef_=''):
        voevent.showIndent(outfile, level)
        added_stuff = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        added_stuff += 'xmlns:voe="http://www.ivoa.net/xml/voevent/v2.0"\n'
        added_stuff += 'xsi:schemaLocation="http://www.ivoa.net/xml/voevent/v2.0 %s"\n' % self.schemaURL

        outfile.write('<%s%s%s %s' % (namespace_, name_,
            namespacedef_ and ' ' + namespacedef_ or '',
            added_stuff,
            ))
#        self.event.exportAttributes(outfile, level, [], namespace_)
        self.event.exportAttributes(outfile, level, [])
        if self.event.hasContent_():
            outfile.write('>\n')
#            self.event.exportChildren(outfile, level + 1, namespace_='', name_)
            self.event.exportChildren(outfile, level + 1, '', name_)
            voevent.showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def stringVOEvent(event, schemaURL = "http://www.ivoa.net/xml/voevent/voevent-v2.0.xsd"):
    '''
    Converts a voevent to a string suitable for output
    '''
    v = VOEventExportClass(event, schemaURL)
    out = StringIO()

    out.write('<?xml version="1.0" ?>\n')
    v.export(out, 0, namespace_='voe:')
    out.write('\n')
    return out.getvalue()

def paramValue(p):
    s1 = p.value
    s2 = p.Value
    if not s2: return s1
    if not s1: return s2
    if len(s1) > len(s2): return s1
    else: return s2

def htmlList(list):
    '''
    Converts a list of strings to an HTML <ul><li> structure.
    '''
    s = '<ul>'
    for x in list:
        s += '<li>' + str(x) + '</li>'
    s += '</ul>'
    return s

def htmlParam(g, p):
    '''
    Builds an HTML table row from a Param and its enclosing Group (or None)
    '''
    s = ''
    if g == None:
        s += '<td/>'
    else:
        s += '<td>' + g.name + '</td>'
    s += '<td>' + str(p.name) + '</td>'
    s += '<td>'
    for d in p.Description: s += str(d)
    s += '</td>'
    s += '<td><b>' + str(paramValue(p)) + '</b></td>'
    s += '<td>' + str(p.ucd) + '</td>'
    s += '<td>' + str(p.unit) + '</td>'
    s += '<td>' + str(p.dataType) + '</td>'
    return s

def parse(file):
    '''
    Parses a file and builds the voevent DOM.
    '''
    doc = voevent.parsexml_(file)
    rootNode = doc.getroot()
    rootTag, rootClass = voevent.get_root_tag(rootNode)
    v = rootClass()
    v.build(rootNode)
    return v

def parseString(inString):
    '''
    Parses a string and builds the voevent DOM.
    '''
    from StringIO import StringIO
    doc = voevent.parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = voevent.get_root_tag(rootNode)
    rootObj = rootClass()
    rootObj.build(rootNode)
    return rootObj

def get_isotime(v):
    assert isinstance(v, voevent.VOEvent)
    try:
        ol = v.WhereWhen.ObsDataLocation.ObservationLocation
        return ol.AstroCoords.Time.TimeInstant.ISOTime
    except:
        return None

def getWhereWhen(v):
    '''
    Builds a dictionary of the information in the WhereWhen section:
    observatory: location of observatory (string);
    coord_system: coordinate system ID, for example UTC-FK5-GEO;
    time: ISO8601 representation of time, for example 1918-11-11T11:11:11;
    timeError: in seconds;
    longitude: in degrees, usually right ascension;
    latitude: in degrees, usually declination;
    positionalError: positional error in degrees.
    '''
    wwd = {}
    ww = v.WhereWhen
    if not ww:
        return wwd
    w = ww.ObsDataLocation
    if not w: 
        return wwd
    ol = w.ObservatoryLocation
    if ol: 
        wwd['observatory'] = ol.id
    ol = w.ObservationLocation
    if not ol:
        return wwd
    observation = ol.AstroCoords
    if not observation: 
        return wwd
    wwd['coord_system'] = observation.coord_system_id
    time = observation.Time
    wwd['time'] = time.TimeInstant.ISOTime
    wwd['timeError'] = time.Error

    pos = observation.Position2D
    if not pos:
        return wwd
    wwd['positionalError']  = pos.Error2Radius
    v2 = pos.Value2
    if not v2:
        return wwd
    wwd['longitude'] = v2.C1
    wwd['latitude']  = v2.C2
    return wwd

def makeWhereWhen(wwd):
    '''
    Expects a dictionary of the information in the WhereWhen section, and makes a 
    voevent.WhereWhen object suitable for set_WhereWhen().
    observatory: location of observatory (string);
    coord_system: coordinate system ID, for example UTC-FK5-GEO;
    time: ISO8601 representation of time, for example 1918-11-11T11:11:11;
    timeError: in seconds;
    longitude: in degrees, usually right ascension;
    latitiude: in degrees, usually declination;
    positionalError: positional error in degrees.
    '''

    if not wwd.has_key('observatory'):     wwd['observatory'] = 'unknown'
    if not wwd.has_key('coord_system'):    wwd['coord_system'] = 'UTC-FK5-GEO'
    if not wwd.has_key('timeError'):       wwd['timeError'] = 0.0
    if not wwd.has_key('positionalError'): wwd['positionalError'] = 0.0

    if not wwd.has_key('time'): 
        print "Cannot make WhereWhen without time"
        return None
    if not wwd.has_key('longitude'):
        print "Cannot make WhereWhen without longitude"
        return None
    if not wwd.has_key('latitude'):
        print "Cannot make WhereWhen without latitude"
        return None

    ac = voevent.AstroCoords(coord_system_id=wwd['coord_system'])

    ac.set_Time(
        voevent.Time(
            TimeInstant = voevent.TimeInstant(wwd['time'])))

    ac.set_Position2D(
        voevent.Position2D(
            Value2 = voevent.Value2(wwd['longitude'], wwd['latitude']),
            Error2Radius = wwd['positionalError']))

    acs = voevent.AstroCoordSystem(id=wwd['coord_system'])

    onl = voevent.ObservationLocation(acs, ac)
    oyl = voevent.ObservatoryLocation(id=wwd['observatory'])
    odl = voevent.ObsDataLocation(oyl, onl)
    ww = voevent.WhereWhen
    ww.set_ObsDataLocation(odl)
    return ww

def get_param_names(v):
    '''
    Takes a voevent and produces a list of pairs of group name and param name.
    For a bare param, the group name is the empty string.
    '''
    list = []
    w = v.What
    if not w: return list
    for p in v.What.Param:
        list.append(('', p.name))
    for g in v.What.Group:
        for p in g.Param:
            list.append((g.name, p.name))
    return list

def findParam(event, groupName, paramName):
    '''
    Finds a Param in a given voevent that has the specified groupName
    and paramName. If it is a bare param, the group name is the empty string.
    '''
    w = event.What
    if not w:
        print "No <What> section in the event!"
        return None
    if groupName == '':
        for p in event.What.Param:
            if p.name == paramName:
                return p
    else:
        for g in event.What.Group:
            if g.Name == groupName:
                for p in event.What.Param:
                    if p.name == paramName:
                        return p
    print 'Cannot find param named %s/%s' % (groupName, paramName)
    return None

######## utilityTable ########################
class utilityTable(voevent.Table):
    '''
    Class to represent a simple Table from voevent
    '''
    def __init__(self, table):
        self.table = table
        self.colNames = []
        self.default = []
        col = 0
        for f in table.Field:
            if f.name:
                self.colNames.append(f.name)
                type = f.dataType
                if type == 'float': self.default.append(0.0)
                elif type == 'int': self.default.append(0)
                else:               self.default.append('')

    def getTable(self):
        return self.table

    def blankTable(self, nrows):
        '''
        From a table template, replaces the Data section with nrows of empty TR and TD
        '''
        data = voevent.Data
        ncol = len(self.colNames)

        for i in range(nrows):
            tr = voevent.TR
            for col in range(ncol):
                tr.add_TD(self.default[col])
            data.add_TR(tr)
        self.table.set_Data(data)

    def getByCols(self):
        '''
        Returns a dictionary of column vectors that represent the table.
        The key for the dict is the Field name for that column.
        '''
        d = self.table.Data
        nrow = len(d.TR)
        ncol = len(self.colNames)

# we will build a matrix nrow*ncol and fill in the values as they
# come in, with col varying fastest.  The return is a dictionary,
# arranged by column name, each with a vector of
# properly typed values.
        data = []
        for col in range(ncol):
            data.append([self.default[col]]*nrow)

        row = 0
        for tr in d.TR:
            col = 0
            for td in tr.TD:
                data[col][row] = td
                col += 1
            row += 1

        dict = {}
        col = 0
        for colName in self.colNames:
            dict[colName] = data[col]
            col += 1
        return dict

    def setValue(self, name, irow, value, out=sys.stdout):
        '''
        Copies a single value into a cell of the table.
        The column is identified by its name, and the row by an index 0,1,2...
        '''
        if name in self.colNames:
            icol = self.colNames.index(name)
        else:
            print>>out, "setTable: Unknown column name %s. Known list is %s" % (name, str(self.colNames))
            return False

        d = self.table.Data
        ncols = len(self.colNames)
        nrows = len(d.TR)

        if nrows <= irow:
            print>>out, "setTable: not enough rows -- you want %d, table has %d. Use blankTable to allocate the table." % (irow+1, nrows)
            return False

        tr = d.TR[irow]
        row = tr.TD
        row[icol] = value
        tr.set_TD(row)

    def toString(self):
        '''
        Makes a crude string representation of a utilityTable
        '''
        s = ' '
        for name in self.colNames:
            s += '%9s|' % name[:9]
        s += '\n\n'

        d = self.table.Data
        for tr in d.TR:
            for td in tr.TD:
                s += '%10s' % str(td)[:10]
            s += '\n'
        return s
