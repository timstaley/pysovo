from collections import namedtuple
#For storage of variables that should not be made publicly available on GitHub,
#e.g. email / phone /  ip addresses etc.
#Be very careful what changes you commit here!

Contact = namedtuple('Contact', ['name', 'email', 'mobile', 'ip_address'])

tim = Contact(name="Tim",
              email="No spam please, interwebs.",
              mobile="441234567890",
              ip_address=None)

ami = Contact(name=None,
              email="No spam please, interwebs.",
              mobile=None,
              ip_address=None)

test = Contact(name="Voevent (test)",
               email=None,
               mobile=None,
              ip_address=None)         

ami_requesters = {"me" : None}

