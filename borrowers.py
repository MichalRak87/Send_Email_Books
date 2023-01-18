import sqlite3
from collections import namedtuple
from tabulate import tabulate
from sql_context_manager import SqlContextManager

sql_connection = sqlite3.connect("database.db")
User = namedtuple("User", "name book_title book_return_at")


def setup(connection):
    with SqlContextManager(connection) as database:
        database.cursor.execute(
            """
        CREATE TABLE
        borrowers
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        book_title TEXT,
        book_return_at DATE
        )
        """
        )


def get_borrowers_by_return_date(connection, book_return_at):
    users_data = []
    with SqlContextManager(connection) as database:
        database.cursor.execute(
            """
        SELECT
        name,
        book_title,
        book_return_at

        FROM
        borrowers

        WHERE
        book_return_at < ?
        """,
            (book_return_at,),
        )
        for name, book_title, book_return_at in database.cursor.fetchall():
            users_data.append(User(name, book_title, book_return_at))
        tab = tabulate(
            users_data, headers=["name", "book_title", "book_return_at"], tablefmt="fancy_grid"
        )
        print(tab)
        return users_data


users = get_borrowers_by_return_date(sql_connection, "2025-01-01")

