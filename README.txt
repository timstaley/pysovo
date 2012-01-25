Basic tools to do things with VOEvents. 
(e.g. pick out certain events, then send email alerts or new VOEvents, etc.)
----------------------------------------------------------------------------------------
Prerequisites:

VOEventLib, for parsing VOEvent xml packets.  
http://lib.skyalert.org/VOEventLib/

Astropysics, for everything else:
http://packages.python.org/Astropysics/index.html
>sudo easy_install astropysics
or
>sudo pip install astropysics

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
*Unit tests (now a priority!)

*Example of using astropysics tools to compute target rise  / set / transit times per observatory.

*Implementation of portfolio class (work in progress)

*Skyalert scraping tools (work in progress)

*Implement "email account" as a class, with "outgoing/SMTP" and "incoming/IMAP" as subclasses.
 Then email_account could do send(), check() - e.g. for communication with the AMI bot.

 


