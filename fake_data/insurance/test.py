import sqlalchemy as db
from insurance.create import Create 
import numpy as np
import pandas as pd
from sqlalchemy.orm import declarative_base as Base

base = Base()

# mysql
engine = db.create_engine(
    'mysql+pymysql://root:@127.0.0.1:3306/practice?unix_socket=/tmp/mysql.sock'
)

class Table(base):

    __tablename__ = "new_table"
    dependent_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    row_info = db.Column(db.Integer())

    def __init__(
        self,
        row_info,
    ):
        self.row_info = row_info

class Table2(base):

    __tablename__ = "new_table2"
    dependent_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    row_info = db.Column(db.Integer())

    def __init__(
        self,
        row_info,
    ):
        self.row_info = row_info


#--------------------------------------------------
meta = db.MetaData()

def User(metadata):
    user = db.Table(
        "user",
        metadata,
        db.Column("user_id", db.Integer, primary_key=True),
        db.Column("user_name", db.String(16), nullable=False),
        db.Column("email_address", db.String(60)),
        db.Column("nickname", db.String(50), nullable=False),
    )
    return user

def User2(metadata):
    user = db.Table(
        "user2",
        metadata,
        db.Column("user_id", db.Integer, primary_key=True),
        db.Column("user_name", db.String(16), nullable=False),
        db.Column("email_address", db.String(60)),
        db.Column("nickname", db.String(50), nullable=False),
    )
    return user

user = User(meta)
user2 = User2(meta)

type(user)

base = Base(metadata=meta)


