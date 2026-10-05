"""
filename: twitter_utils.py
Requires the driver:  conda install mysql-connector-python
A collection of database utilities to make it easier to implement a database application
"""

import mysql.connector
import pandas as pd

# Created a utility class to handle database interactions
class TwitterUtils:

    def __init__(self, user, password, database, host="localhost", port=4300):
        """ Future work: Implement connection pooling """
        self.con = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
    # Function to close the connection to the database
    def close(self):
        """ Close or release a connection back to the connection pool """
        self.con.close()
        self.con = None

    #function to execute a select query and return the result as a dataframe
    def execute(self, query):
        """ Execute a select query and returns the result as a dataframe """

        # Step 1: Create cursor
        rs = self.con.cursor()

        # Step 2: Execute the query
        rs.execute(query)

        # Step 3: Get the resulting rows and column names
        rows = rs.fetchall()
        cols = list(rs.column_names)

        # Step 4: Close the cursor
        rs.close()

        # Step 5: Return result
        return pd.DataFrame(rows, columns=cols)

    # Function to insert a single row into the database
    def insert_one(self, sql, val):
        """ Insert a single row """
        cursor = self.con.cursor()
        cursor.execute(sql, val)
        self.con.commit()

    # Function to insert multiple rows into the database
    def insert_many(self, sql, vals):
        """ Insert multiple rows """
        cursor = self.con.cursor()
        cursor.executemany(sql, vals)
        self.con.commit()



