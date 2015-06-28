from collections import namedtuple

EmailContact = namedtuple('EmailContact', 'name email')
VoeventContact = namedtuple('VoeventContact', 'name ipaddress port')

alex = EmailContact(name='Alex Smith', email='alex.smith@university.ac.uk')
jo = EmailContact(name='Jo Blogs', email='jo.blogs@university.ac.uk')

grb_contacts = [alex, jo]
test_contacts = [alex]

local_vobroker = VoeventContact(name='local_vobroker',
                                ipaddress='localhost', port=8098)
