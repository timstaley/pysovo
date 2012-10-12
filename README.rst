========
pysovo
========

Basic tools to do things with VOEvents. 
(e.g. pick out certain events, then send email alerts or new VOEvents, etc.)

---------------
Prerequisites:
---------------

 - `VOEventLib <http://lib.skyalert.org/VOEventLib/>`_, for parsing VOEvent xml packets.  
 - `Astropysics <http://packages.python.org/Astropysics/>`_, for everything else. **NB I have applied some minor fixes which are not yet pulled into master**, 
   so for now you will need my `fork <https://github.com/timstaley/astropysics/tree/pysovo-compatible-2012-10-12>`_.
 - If you want to make use of SMS alerts, you will also need `textmagic-sms-api-python <http://code.google.com/p/textmagic-sms-api-python/>`_.
   This is a user-friendly interface to the SMS api provided by textmagic.com.

------------------
Setup:
------------------

If you want to use the email alert facility, you should run

``>$ python input_email_settings.py``

This will prompt you for username, password (input hidden on a plain terminal) etc. 
The details are saved under ``$HOME/.vo_alerts/email_acc``
and the file permissions are set so that only you have read access. 
(This file is also easy to edit manually, 
but then your password will of course show up in plain text on screen.)
*NB* The email facility has only been tested with Gmail- 
the server handshake may need hacking at for other email services.

------------------------------------------------------------------------------------
Testing:
------------------------------------------------------------------------------------
There are currently a few unit tests, try 
nosetests -svx from the ``pysovo`` package folder.

Also see the ``integration_tests`` folder.

-------------------------------------------------------------------------------------
To do:
-------------------------------------------------------------------------------------

 * More Unit tests
 * Implementation of portfolio class (work in progress)
 * Skyalert scraping tools (work in progress)
 * Implement email "incoming/IMAP"- e.g. for 2 way communication with an observatory bot.

 

