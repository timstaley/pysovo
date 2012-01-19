#from VOEventLib import Vutil as voe_utils

from pysovo import voe, voe_utils


import pprint

testfilename="test_data/GBM_Alert_2011-06-13T15_08_46.30_329670528_1-006.xml"

 
v=voe_utils.parse(testfilename)


assert isinstance(v, voe.VOEvent)


pp = pprint.PrettyPrinter()
pp.pprint( voe_utils.getWhereWhen(v) )

#v.What
print "Param names:"
pp.pprint(voe_utils.get_param_names(v))
print "[End Param names]"
who=v.Who
assert isinstance(who, voe.Who)

w=v.What
assert isinstance(w, voe.What)

all_params= {i.name : (i.value, i.unit, i.ucd) 
             for i in w.Param}

sub_params = {}
for g in w.Group:
    sub_params.update(
          {"---".join((g.name,i.name)) : (i.value, i.unit, i.ucd) for i in g.Param}
          )
    
all_params.update(sub_params)
#print all_params
pp.pprint(all_params)

with open("testout1.xml",'w') as testout:
    testout.write(voe_utils.stringVOEvent(v))

lochan = voe_utils.findParam(v, "", "Lo_Chan_Index")
assert isinstance(lochan, voe.Param)
print "Low channel index:", lochan.value
lochan.value = 42

with open("testout2.xml",'w') as testout:
    testout.write(voe_utils.stringVOEvent(v))



