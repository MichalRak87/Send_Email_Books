"""
Module take data from database and send e-mail by return date
"""
import sqlite3
from collections import namedtuple
from os import getenv
from string import Template
from dotenv import load_dotenv
from emails import EmailSender
from borrowers import get_borrowers_by_return_date

load_dotenv()

# Environ data
ssl_enabled = bool(int(getenv("TRAP_SSL_ENABLED")))
port = int(getenv("TRAP_PORT"))
smtp_server = getenv("TRAP_SMTP_SERVER")
username = getenv("TRAP_USERNAMES")
password = getenv("TRAP_PASSWORD")
sender = getenv("SENDER")
subject = getenv("SUBJECT")

# Credentials:
Credentials = namedtuple("Credentials", "username password")
credentials = Credentials(username, password)

# Database connection:
sql_connection = sqlite3.connect(getenv("DATABASE"))

# Message text:
message_text = Template(
    """
Witaj $imie,
Biblioteka publiczna wzywa Cie do oddanie książki pod tytułem: $tytul_ksiazki.
Termin zwrotu minął w dniu: $termin_zwrotu

W razie jakichkolwiek problemów prosimy o kontakt e-mail:
E-mail: $sender

Wiadomość generowana automatycznie, prosimy nie odpowiadać.

Pozdrawiamy biblioteka publiczna""")


def run():
    """
    Function start program
    :return: None
    """
    users = get_borrowers_by_return_date(sql_connection, "2023-01-01")
    with EmailSender(port, smtp_server, credentials, ssl_enabled=ssl_enabled) as email:
        for user_list in users:
            text = message_text.substitute(
                imie=user_list.name,
                tytul_ksiazki=user_list.book_title,
                termin_zwrotu=user_list.book_return_at,
                sender=sender,
            )
            email.send_mail(sender, user_list.e_mail, subject, text)


if __name__ == "__main__":
    run()
