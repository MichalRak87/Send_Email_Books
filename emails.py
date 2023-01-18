import logging
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

logging.basicConfig(level=logging.INFO)
date_format = "%Y-%m-%d %H:%M:%S"


class EmailSender:
    logging.info(f"Start time: {datetime.now().strftime(date_format)}")

    def __init__(self, port, smtp_server, credentials, ssl_enabled=False):
        self.ssl_enabled = ssl_enabled
        self.smtp_server = smtp_server
        self.port = port
        self.connection = None
        self.credentials = credentials
        self.sender = None
        self.receiver = None
        self.subject = None
        logging.info(f"__init__ = OK")

    def __enter__(self):
        if not self.ssl_enabled:
            self.connection = smtplib.SMTP(self.smtp_server, self.port)
            logging.info(f"SSL = {self.ssl_enabled}")
        else:
            context = ssl.create_default_context()
            self.connection = smtplib.SMTP_SSL(self.smtp_server, self.port, context=context)
            logging.error("__enter__ self.connection = SSL")
        self.connection.login(self.credentials.username, self.credentials.password)
        logging.debug(
            f"Logging: (Username: {self.credentials.username},Password: {self.credentials.password})"
        )
        return self

    def send_mail(self, sender, receiver, subject, message_text):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        message = EmailMessage()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = subject
        message.set_content(message_text)
        self.connection.sendmail(sender, receiver, message.as_string())

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not isinstance(exc_val, Exception):
            logging.info(
                f"Message From: {self.sender} To: {self.receiver}"
                f" Subject: {self.subject} has sent"
            )
        else:
            logging.exception(f"Exception{exc_val}")
        self.connection.close()
        logging.info(f"Connection closed | {datetime.now().strftime(date_format)}")
