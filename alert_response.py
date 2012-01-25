#!/usr/bin/python
import sys
from VOEventLib import VOEvent as voe, Vutil as voe_utils
from pysovo import observatories, utils

class alert_tags:
    swift_grb="swift_grb"

def main():
    s = sys.stdin.read()
    v = voe_utils.parseString(s)
    
    #SWIFT BAT GRB alert:
    if v.ivorn.find("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos")==0:
        swift_bat_grb_logic(v)
        
    return 0

def swift_bat_grb_logic(v):
    swift_ivorn_id = v.ivorn[len("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_"):]
    posn = utils.pull_FK5_from_WhereWhen(v)
    if posn.dec.degrees >-10.0:
        observatories.ami.send_alert(posn,
                                     alert_tags.swift_grb,
                                     swift_ivorn_id)
    else:
        pass
    
if __name__=='__main__':
    sys.exit(main())
    
