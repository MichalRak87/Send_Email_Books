"""
Email context manager
"""
import logging
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime


logging.basicConfig(level=logging.ERROR)
FORMATTED_DATE = "%Y-%m-%d %H:%M:%S"


class EmailSender:
    """
    Email context manager
    """

    logging.info("Start time: %s}", datetime.now().strftime(FORMATTED_DATE))

    def __init__(self, port, smtp_server, credentials, ssl_enabled=False):
        self.ssl_enabled = ssl_enabled
        self.smtp_server = smtp_server
        self.port = port
        self.connection = None
        self.credentials = credentials
        logging.info("__init__ = OK")

    def __enter__(self):
        if not self.ssl_enabled:
            self.connection = smtplib.SMTP(self.smtp_server, self.port)
            logging.info("SSL = %s", self.ssl_enabled)
        else:
            context = ssl.create_default_context()
            self.connection = smtplib.SMTP_SSL(self.smtp_server, self.port, context=context)
            logging.error("__enter__ self.connection = SSL")
        self.connection.login(self.credentials.username, self.credentials.password)
        logging.debug(
            "Logging: (Username: %s,Password: %s",
            self.credentials.username,
            self.credentials.password,
        )
        return self

    def send_mail(self, sender, receiver, subject, message_text):
        """
        Function send_email needs 4 param sender, receiver and subject message_text
        :param sender: str: name surname <e-mail>
        :param receiver: str: name surname <e-mail>
        :param subject: str: e-mail subject
        :param message_text: str: message
        :return: None
        """
        message = EmailMessage()
        message.set_charset("utf-8")
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = subject
        message.set_content(message_text)
        self.connection.sendmail(sender, receiver, message.as_string())
        logging.info(
            "Message From: %s To: %s Subject: %s has been created", sender, receiver, subject
        )
        print(f"Message to {receiver} has been sent correctly")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            logging.exception("Exception %s", exc_val)
        self.connection.close()
        logging.info("Connection closed : %s", datetime.now().strftime(FORMATTED_DATE))
