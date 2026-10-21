import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhav@2006",
        database="dml"
    )

    return connection