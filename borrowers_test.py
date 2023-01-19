"""
Module testing borrowers.py
"""
import sqlite3
from pytest import fixture
from borrowers import get_borrowers_by_return_date


@fixture(name='create_cursor_fixture')
def create_cursor():
    """
    Fixture create test database in memory
    :return: connection
    """
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
             book_return_at DATE,
             e_mail DATE
             )
             """
    )

    sample_data = [
        (1, "Michal", "Ogniem i mieczem", "2021-12-01", 'michal@test.pl'),
        (2, "Pawel", "Potop", "2022-01-01", 'pawel@test.pl'),
        (3, "Alan", "Lalka", "2023-10-11", 'alan@test.pl'),
        (4, "Ola", "Quo Vadis", "2023-11-06", 'ola@test.pl'),
    ]
    cursor.executemany(
        """
    INSERT INTO
    borrowers
    VALUES
    (?,?,?,?,?)
    """,
        sample_data,
    )

    return connection


def test_borrowers(create_cursor_fixture):
    """
    Test function get_borrowers_by_return_date(connection, date)
    :param create_cursor_fixture: connection with database in memory
    :return: None
    """
    users = get_borrowers_by_return_date(create_cursor_fixture, "2023-01-01")

    assert len(users) == 2
    assert users[0].name == "Michal"
    assert users[1].name == "Pawel"
    assert users[0].e_mail == 'michal@test.pl'
    assert users[1].e_mail == 'pawel@test.pl'
