import sqlite3

connection = sqlite3.connect('database.db',check_same_thread=False)

current_conn = connection.cursor()
connection.row_factory = sqlite3.Row
current_conn.execute("CREATE TABLE IF NOT EXISTS movieReview(ID INTEGER PRIMARY KEY AUTOINCREMENT, Review text,Prediction text, Userfeedback text);")


def get_connection():

    return (connection, current_conn)

def close_connection():
    connection.close()

