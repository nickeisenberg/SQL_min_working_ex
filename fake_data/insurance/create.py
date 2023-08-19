import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import declarative_base as Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
import datetime as dt
import faker
import numpy as np
from insurance.constants import JOBS, SALARY_AVG

_fk = faker.Faker()
_base = Base()

class Mailing(_base):
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



class Employment(_base):
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

class Finances(_base):
    # table name for User model
    __tablename__ = "finances"

    # user columns
    person_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    bank_act = db.Column(db.String(20))
    savings = db.Column(db.Integer())
 
    def __init__(self, bank_act, savings):
        self.bank_act = bank_act
        self.savings = savings

class Dependents(_base):

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


def salary_generator(avg_sal):
    if avg_sal == 0:
        return 0
    else:
        sal_noise = max(
            np.random.gamma(.1, avg_sal) - np.random.gamma(.1, avg_sal),
            -1. * avg_sal / 2
        )
        return avg_sal + sal_noise


def savings_generator(avg_sal):
    if avg_sal == 0:
        return np.random.gamma(.5, 50) - np.random.gamma(.1, 50)
    else:
        saving = np.random.normal(
            avg_sal * 4,
            avg_sal * 1.5,
        )
        return saving


def startdate_generator(
        start=dt.datetime(2000, 1, 1),
        end=dt.datetime(2023, 8, 15)):
    start_date = dt.datetime.strftime(
        _fk.date_between(start, end), '%Y-%m-%d'
    )
    return start_date


def dependent_generator():
    return int(abs(np.random.gamma(1, 1.3)))


class Create:

    def __init__(
        self,
        base=_base,
        Mailing=Mailing,
        Employment=Employment,
        Finances=Finances,
        Dependents=Dependents
    ):
        self.base = base
        self.Mailing = Mailing
        self.Employlment = Employment 
        self.Finances = Finances 
        self.Dependents = Dependents
        self._initialized = False


    def initialize(self, engine, no_entries):
        if self._initialized:
          raise Exception("Database already initialized.")

        if database_exists(engine.url):
            drop_database(engine.url) 
        if not database_exists(engine.url):
            create_database(engine.url) 

        self.base.metadata.create_all(bind=engine)

        self._initialized = True

        session  = sessionmaker(bind=engine)()
        for i in range(no_entries):
            mailing = Mailing(
                _fk.first_name(),
                _fk.last_name(),
                _fk.street_address(),
                _fk.city(),
                _fk.state(),
                _fk.zipcode(),
            )
            session.add(mailing)
            job = np.random.choice(JOBS)
            employment = Employment(
                salary_generator(SALARY_AVG[job]),
                job,
                startdate_generator()
            )
            session.add(employment)
            finances = Finances(
                _fk.bban(),
                savings_generator(SALARY_AVG[job]),
            )
            session.add(finances)
            num_dependents = dependent_generator()
            if num_dependents > 0:
                for dep in range(num_dependents):
                    dependents = Dependents(
                        policyholder_id=int(i + 1),
                        first_name=_fk.first_name(),
                        last_name=_fk.last_name(),
                        same_residence=[False, True][np.random.binomial(1, .8)],
                        is_student=[False, True][np.random.binomial(1, .8)],
                        is_employed=[False, True][np.random.binomial(1, .6)]
                    )
                    session.add(dependents)
        session.commit()

        return None
