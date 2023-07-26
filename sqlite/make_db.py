import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base as Base
import sqlite3
import faker
import numpy as np

f = faker.Faker()

# set up the classes to make the tables and add the rows
base = Base()

class personal_info(base):
    __tablename__='personal_info'
    id = sql.Column(
        sql.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    first_name = sql.Column(sql.VARCHAR(200))
    last_name = sql.Column(sql.VARCHAR(200))
    address = sql.Column(sql.VARCHAR(200))
    city = sql.Column(sql.VARCHAR(200))
    state = sql.Column(sql.VARCHAR(200))
    zipcode = sql.Column(sql.VARCHAR(200))
    def __init__(self):
        self.first_name = f.first_name()
        self.last_name = f.last_name()
        self.address = f.street_address()
        self.city = f.city()
        self.state = f.state()
        self.zipcode= f.postcode()

items = ['car', 'house', 'sofa', 'tv']
class item_purchased(base):
    __tablename__ = 'item_purchased'
    id = sql.Column(
        sql.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    item = sql.Column(sql.VARCHAR(200))
    def __init__(self):
        self.item = items[np.random.randint(0, 4)]

# set up the connection to the datebase.
engine = sql.create_engine('sqlite:///purchases.db')
base.metadata.create_all(bind=engine)

# add the rows
session  = sessionmaker(bind=engine)()
for i in range(1):
    pers = personal_info()
    it = item_purchased()
    session.add(pers)
    session.add(it)
session.commit()

# read the rows from the tables
con = sqlite3.connect('purchases.db')

cursor = con.execute('select * from personal_info')
for row in cursor:
    print(row)

cursor = con.execute('select * from item_purchased')
for row in cursor:
    print(row)

