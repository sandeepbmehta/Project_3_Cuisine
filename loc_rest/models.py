# from app import db

# class Hist(db.Model):
#     __tablename__ = 'hist'

#     id = db.Column(db.Integer, primary_key=True)
#     addressline1 = db.Column(db.String(64))
#     addressline2 = db.Column(db.String(64))
#     zipcode = db.Column(db.Integer)
#     cusine = db.Column(db.String(64))

#     def __repr__(self):
#         return '<Hist %r>' % (self.name)

# import necessary libraries
# from bs4 import BeautifulSoup
# import requests
# import pprint
# import json
# from sqlalchemy import func
# import os
# from flask_sqlalchemy import SQLAlchemy

# engine = create_engine("sqlite:///db/hist.sqlite")  # Access the DB Engine
# if not engine.dialect.has_table(engine, hist):  # If table don't exist, Create.
#     metadata = MetaData(engine)
#     # Create a table with the appropriate Columns
#     Table(hist, metadata,
#           Column('Id', Integer, primary_key=True, nullable=False), 
#           Column('addressline1', String), Column('addressline2', String),
#           Column('zipcode', String), Column('cusine', String),
#     # Implement the creation
#     metadata.create_all()
#      )

    
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
 
if __name__ == '__main__':
    create_connection("sqlite:///db/hist.sqlite")
