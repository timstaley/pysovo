Basic tools to do things with VOEvents. 
(e.g. pick out certain events, then send email alerts or new VOEvents, etc.)
----------------------------------------------------------------------------------------
Prerequisites:

VOEventLib, for parsing VOEvent xml packets.  
http://lib.skyalert.org/VOEventLib/

Astropysics, for everything else. NB currently I have applied some minor fixes, until these are accepted by Erik you should grab my fork:
https://timstaley@github.com/timstaley/astropysics.git
and checkout the commit: ef5c270c35c34e4ebb0da7dc5257545ea6590bf9


If you want to make use of SMS alerts, you will also need textmagic-sms-api-python
http://code.google.com/p/textmagic-sms-api-python/
-This is a well written interface to the SMS api provided by www.textmagic.com

---------------------------------------------------------------------------------------
Setup:

If you want to use the email alert facility, you should run
>$ python input_email_settings.py

This will prompt you for username, password (input hidden on a plain terminal) etc. 
The details are saved under $HOME/.vo_alerts/email_acc
and the file permissions are set so that only you have read access. 
(This file is also easy to edit manually, 
but then your password will show up in plain text on screen!)
NB Only tested with Gmail- 
The server handshake may need hacking at for other email services.

------------------------------------------------------------------------------------
Testing:
After running the email config, you can then edit and run "sendmail_test.py".
Also try tinkering with "parse_event_packet.py"

To test the alert_response, simply feed it an xml packet via stdin, e.g.
>$ cat test_data/BAT_GRB_Pos_511611-746.xml | ./alert_response.py

-------------------------------------------------------------------------------------
To do:
*More Unit tests


*Implementation of portfolio class (work in progress)

*Skyalert scraping tools (work in progress)

*Implement email "incoming/IMAP"- e.g. for 2 way communication with an observatory bot.

 


