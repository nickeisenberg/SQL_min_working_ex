import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import declarative_base as Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

base = Base()

class Mailing(base):
    # table name for User model
    __tablename__ = "mailing"

    # user columns
    person_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    zip = db.Column(db.Integer())
 
    def __init__(
        self,
        first_name,
        last_name,
        address,
        city,
        state,
        zip
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

class Employment(base):
    # table name for User model
    __tablename__ = "employment"

    # user columns
    person_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    job = db.Column(db.String(50))
    salery = db.Column(db.Integer())
    start_date = db.Column(db.String(10))
 
    def __init__(self, salery, job, start_date):
        self.salery = salery
        self.job = job
        self.start_date = start_date

class Finances(base):
    # table name for User model
    __tablename__ = "finances"

    # user columns
    person_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    bank_act = db.Column(db.String(20))
    savings = db.Column(db.Integer())
 
    def __init__(self, bank_act, savings):
        self.bank_act = bank_act
        self.savings = savings

class Dependents(base):

    __tablename__ = "dependents"
    dependent_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    policyholder_id = db.Column(db.Integer())
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    same_residence = db.Column(db.Boolean())
    is_student = db.Column(db.Boolean())
    is_employed = db.Column(db.Boolean())

    def __init__(
        self,
        policyholder_id,
        first_name,
        last_name,
        same_residence,
        is_student,
        is_employed,
    ):
        self.policyholder_id = policyholder_id 
        self.first_name = first_name
        self.last_name = last_name
        self.same_residence = same_residence
        self.is_student = is_student
        self.is_employed = is_employed


# to mysql
engine = db.create_engine(
    'mysql+pymysql://root:@127.0.0.1:3306/practice?unix_socket=/tmp/mysql.sock'
)

if database_exists(engine.url):
    drop_database(engine.url) 
if not database_exists(engine.url):
    create_database(engine.url) 

base.metadata.create_all(bind=engine)


# sqlite
# path = '/Users/nickeisenberg/GitRepos/DataSets_local/test.db'
# engine = db.create_engine(f'sqlite:///{path}')

# base.metadata.create_all(bind=engine)

