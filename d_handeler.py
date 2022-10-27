from optparse import Values
import sqlite3


class data:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("rabbit.db")
        self.conn.row_factory = sqlite3.Row
    # create function
    def create(self):
        c = self.conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS
         tabrabbit(first_name text, last_name text, phone integer)"""
        )
        self.conn.commit()
    # insert data to database

    def insert(self, **kwargs):
        c = self.conn.cursor()
        c.execute(
            f"""INSERT INTO tabrabbit (first_name, last_name, phone) values 
            {kwargs['Fname'],kwargs['Lname'],kwargs['phone']}"""
        )
        self.conn.commit()
        result =c.execute("""SELECT * FROM tabrabbit""").fetchall()[-1]
        print(result)
        self.conn.close()
        return result