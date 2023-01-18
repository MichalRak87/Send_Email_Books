import sqlite3
from pytest import fixture
from borrowers import get_borrowers_by_return_date


@fixture
def create_cursor():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute(
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

    sample_data = [
        (1, "Michal", "Ogniem i mieczem", "2021-12-01"),
        (2, "Pawel", "Potop", "2022-01-01"),
        (3, "Alan", "Lalka", "2023-10-11"),
        (4, "Ola", "Quo Vadis", "2023-11-06"),
    ]
    cursor.executemany(
        """
    INSERT INTO
    borrowers
    VALUES
    (?,?,?,?)
    """,
        sample_data,
    )

    return connection


def test_borrowers(create_cursor):
    users = get_borrowers_by_return_date(create_cursor, "2023-01-01")

    assert len(users) == 2
    assert users[0].name == "Michal"
    assert users[1].name == "Pawel"
