from collections import namedtuple

EmailContact = namedtuple('EmailContact', 'name email')
VoeventContact = namedtuple('VoeventContact', 'name ipaddress port')
EmailLogin = namedtuple('EmailLogin',
                        'username password smtp_server smtp_port')

alex = EmailContact(name='Alex Smith', email='alex.smith@university.ac.uk')
jo = EmailContact(name='Jo Blogs', email='jo.blogs@university.ac.uk')

grb_contacts = [alex, jo]
test_contacts = [alex]

local_vobroker = VoeventContact(name='local_vobroker',
                                ipaddress='localhost', port=8098)

sendgrid_api_key = "Paste sendgrid API key here"
sendgrid_bcc_address = 'foo.bar+sentviasendgrid@gmail.com'

gmail_login = EmailLogin(username='foo.bar@gmail.com',
                         password='foobarbaz',
                         smtp_server='smtp.googlemail.com',
                         smtp_port=587
                         )
