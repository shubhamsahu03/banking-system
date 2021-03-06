import mysql.connector
import os.path


def initialize_db():
    credentials_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "mysqlcredentials.txt"
    )

    with open(credentials_path, "r") as f:
        output = [line.strip("\n") for line in f.readlines()]

    db = mysql.connector.connect(
        host=output[0],
        port=output[1],
        user=output[2],
        passwd=output[3],
    )
    cursor = db.cursor()

    # Create bank database
    query = """CREATE DATABASE IF NOT EXISTS bank"""
    cursor.execute(query)
    db.commit()

    # Create bank.users table
    query = """
    CREATE TABLE IF NOT EXISTS bank.users
    (
        firstname VARCHAR(16) NOT NULL,
        lastname VARCHAR(16) NOT NULL,
        accno INT(6) PRIMARY KEY AUTO_INCREMENT,
        passwd VARCHAR(32) NOT NULL,
        date_created DATETIME NOT NULL DEFAULT NOW(),
        balance INT NOT NULL DEFAULT 0
    )
    """
    cursor.execute(query)
    db.commit()

    query = """ALTER TABLE bank.users AUTO_INCREMENT=100000"""
    cursor.execute(query)
    db.commit()

    # Create bank.transactionhistory table
    query = """
    CREATE TABLE IF NOT EXISTS bank.transactionhistory
    (
        user1accno INT(6),
        user2accno INT(6),
        amount INT NOT NULL,
        time_of_transaction DATETIME NOT NULL DEFAULT NOW(),
        FOREIGN KEY (user1accno) REFERENCES bank.users(accno)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (user2accno) REFERENCES bank.users(accno)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )"""
    cursor.execute(query)
    db.commit()

    db.close()
