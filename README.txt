VOEvent parsers derived from the VOEventLib - see http://lib.skyalert.org/VOEventLib/

Let me know if you also want the modified libgen code,
used to generate voe.py from the schema.
----------------------------------------------------------------------------------------
Prerequisites:
"angles" (for sexagesimal formatting, etc.) -- try
>$ easy_install angles

or goto http://pypi.python.org/pypi/angles/1.1

---------------------------------------------------------------------------------------
Setup:

If you want to use the email alert facility, you should run
>$ python input_email_settings.py

This will prompt you for username, password (hidden) etc. The details are saved under
$HOME/.vo_alerts/email_acc
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
*Implementation of portfolio class (work in progress)

*Skyalert scraping tools (work in progress)

*Unit tests

*Conversion of member variable names to python style e.g. v.where_when. 
Unfortunately this will break existing code so needs to be done soon or not at all.

*Conversion of examples from the old VOEvent lib, 
e.g. how to create voevent xml packet from scratch.

 


