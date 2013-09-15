======
pysovo
======

Basic tools to do things with VOEvents. 
(e.g. pick out certain events, then send email alerts or new VOEvents, etc.)

pysovo is not really meant as a general release, it is very much tailored
to our specific needs. However, it may serve as a reference example to others
wishing to get started with VOEvents. 
(And if you want to send custom formatted emails, it's your lucky day.)

For an example of how pysovo is being applied, see
`Staley et al (2012) <http://ukads.nottingham.ac.uk/abs/2012arXiv1211.3115S>`_.

Installation:
-------------
From the command line::

 git clone git@github.com:timstaley/pysovo.git
 cd pysovo
 pip install .


Setup:
------

If you want to use the email alert facility, you should run::

 >$ python input_email_settings.py

This will prompt you for username, password, etc. You can mostly accept default
settings if using a gmail login. Note that the password input will not be
echoed to the terminal if running from a regular python interpreter, but it 
seems that ipython insists on displaying it for you. 
The details are saved under ``$HOME/.vo_alerts/email_acc``
and the file permissions are set so that only you have read access. Your password
will also be weakly obfuscated using base64 encoding. 

.. warning::

 The email routines have only been tested with Gmail- 
 the server handshake may need hacking at for other email services.


Testing:
--------
There are currently a few unit tests, try 
nosetests -svx from the ``pysovo`` package folder.

Also see the ``integration_tests`` folder - the easiest way to get these to 
run prior to installation is to use ipython from the root project folder, 
e.g. ::

  ipython integration_tests/sendmail_test.py


To do:
------
 - Implement email reading, for 2 way communication with AMI.

 
