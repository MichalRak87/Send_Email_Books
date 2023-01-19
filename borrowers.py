"""
Database Module
"""
from collections import namedtuple
from tabulate import tabulate
from sql_context_manager import SqlContextManager


User = namedtuple("User", "name book_title book_return_at e_mail")


def setup(connection):
    """
    Setup function create table 'borrowers' with 5 columns:
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        book_title TEXT,
        book_return_at DATE,
        e_mail TEXT
    :param connection: connection with database
    :return: None
    """
    with SqlContextManager(connection) as database:
        database.cursor.execute(
            """
        CREATE TABLE
        borrowers
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        book_title TEXT,
        book_return_at DATE,
        e_mail TEXT
        )
        """
        )


def get_borrowers_by_return_date(connection, return_date):
    """
    Function print tabulated data from database
    Function return list of namedtuple
    :param connection: connection with database
    :param return_date: date %Y:%m:%d
    :return: List of namedtuple
    """
    users_data = []
    with SqlContextManager(connection) as database:
        database.cursor.execute(
            """
        SELECT
        name,
        book_title,
        book_return_at,
        e_mail

        FROM
        borrowers

        WHERE
        book_return_at < ?
        """,
            (return_date,),
        )
        for name, book_title, book_return_at, e_mail in database.cursor:
            users_data.append(User(name, book_title, book_return_at, e_mail))
        tab = tabulate(
            users_data, headers=["Name", "Book title",
                                 "Book return date",
                                 'E-mail'],
            tablefmt="fancy_grid"
        )
        print(tab)
        return users_data
