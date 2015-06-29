from __future__ import absolute_import
import smtplib
import sendgrid
from sendgrid import SendGridClient
import pysovo as ps
import logging

logger = logging.getLogger(__name__)

from pysovo.local import contacts


class EmailConfigKeys():
    username = 'username'
    password = 'password'
    smtp_server = 'smtp_server'
    smtp_port = 'smtp_port'


keys = EmailConfigKeys()


def send_email_by_smtp(recipient_addresses,
                       subject,
                       body_text,
                       account=contacts.gmail_login
                       ):
    """
    Send email using a Gmail SMTP login.
    """

    logger.debug("Loaded account, starting SMTP session")

    recipient_addresses = ps.utils.listify(recipient_addresses)

    smtpserver = smtplib.SMTP(account.smtp_server,
                              account.smtp_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(account.username,
                     account.password)

    sender = account.username

    recipients_str = ",".join(recipient_addresses)

    logger.debug("Logged in, emailing " +recipients_str)
    header = "".join(['To: ', recipients_str, '\n',
                      'From: ', sender, '\n',
                      'Subject: ', subject, '\n'])

    msg = "".join([header, '\n',
                   body_text, '\n\n'])
    smtpserver.sendmail(sender, recipient_addresses, msg)
    logger.debug('Message sent')
    smtpserver.close()


def send_email_by_sendgrid(
        recipient_addresses,
        subject,
        body_text,
        sg_client=SendGridClient(contacts.sendgrid_api_key,raise_errors=True)
    ):
    """
    Send an email using the Sendgrid API.

    Sendgrid has no storage equivalent of a 'sent' folder,
    so we always BCC a copy to the gmail login with the
    "+sent" alias suffix.
    """

    message = sendgrid.Mail(to=recipient_addresses,
                            subject=subject,
                            html=None,
                            text=body_text,
                            from_email=contacts.gmail_login.username,
                            bcc=contacts.sendgrid_bcc_address)
    status, msg = sg_client.send(message)


def send_email(
        recipient_addresses,
        subject,
        body_text
    ):
    """
    Defines the default delivery method
    """
    # send_email_by_sendgrid(recipient_addresses,subject,body_text)
    send_email_by_smtp(recipient_addresses,subject,body_text)


def dummy_email_send_function(recipient_addresses,
                              subject,
                              body_text
                              ):
    print "*************"
    print "Would have sent an email to:"
    print ps.utils.listify(recipient_addresses)
    print "Subject:", subject
    print "--------------"
    print body_text
    print "*************"
