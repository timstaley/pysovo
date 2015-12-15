from __future__ import absolute_import
import pysovo.triggers.swift
from pysovo.voevent import ivorn_base, test_trigger_substream



def is_test_trigger(voevent):
    ivorn  = voevent.attrib['ivorn']
    if ivorn.startswith("ivo://"+ ivorn_base+'/'+test_trigger_substream+'#'):
        return True
    return False



