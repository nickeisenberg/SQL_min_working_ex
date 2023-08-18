import faker
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy as db

no_entries = 5
fk = faker.Faker()
# engine = db.create_engine(
#     'mysql+pymysql://root:@127.0.0.1:3306/practice?unix_socket=/tmp/mysql.sock'
# )

# Mailing table
#--------------------------------------------------
# names and addresses
first_names = np.array([fk.first_name() for i in range(no_entries)])
last_names = np.array([fk.last_name() for i in range(no_entries)])
address = np.array([fk.street_address() for i in range(no_entries)])
city = np.array([fk.city() for i in range(no_entries)])
state = np.array([fk.state() for i in range(no_entries)])
zipcode = np.array([fk.zipcode() for i in range(no_entries)])
person_id = np.arange(1, no_entries + 1)

columns=[
    'person_id', 'first_name', 'last_name', 'address', 'city', 'state', 'zip'
]
data=np.vstack(
    [person_id, first_names, last_names, address, city, state, zipcode]
).T
mailing_df = pd.DataFrame(data=data, columns=columns)

mailing_df.head()

# mailing_df.to_sql('mailing', engine, index=False, if_exists='append')
#--------------------------------------------------

import numpy as np

avg_sal = 100
vars = []
for i in range(1000):
    vars.append(np.random.gamma(.01, avg_sal) - np.random.gamma(.01, avg_sal))
vars = np.array(vars)

vars.max()

# Employment table
#--------------------------------------------------
# Jobs
faker.Faker.seed(0)
JOBS = [fk.job() for i in range(15)]
JOB_ID = {j: i + 1 for i, j in enumerate(JOBS)}
SALARY_AVG = np.array([
    35, 95, 65, 210, 45, 95, 165, 120, 44, 76, 55, 67, 43, 84, 29
])
SALARY_AVG = {j: s for j, s in zip(JOBS, SALARY_AVG)}
SALARY_AVG['unemployed'] = 0

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
        fk.date_between(start, end), '%Y-%m-%d'
    )
    return start_date

def dependent_generator():
    return int(abs(np.random.gamma(1, 1.3)))


saleries = []
savings = []
jobs = []
for i in range(no_entries):
    job = np.random.choice(JOBS)
    jobs.append(job)
    saleries.append(int(salary_generator(SALARY_AVG[job])))
    savings.append(int(savings_generator(SALARY_AVG[job])))
saleries = np.array(saleries).astype(float)
savings = np.array(savings).astype(float)
jobs = np.array(jobs)

# job start date
start_dates = np.array(
    [startdate_generator() for i in range(no_entries)]
).astype(str)

columns=[
    'person_id', 'job', 'salery', 'start_date'
]
data = np.vstack(
    [person_id, jobs, saleries.astype(int), start_dates]
).T
employment_df = pd.DataFrame(data=data, columns=columns)

# employment_df.to_sql('employment', engine, index=False, if_exists='append')
#--------------------------------------------------

# Savings table
#--------------------------------------------------
# bank_act number
bank_act = np.array([fk.bban() for i in range(no_entries)])
columns=[
    'person_id', 'bank_act', 'savings'
]
data = np.vstack(
    [person_id, bank_act, savings.astype(int)]
).T
savings_df = pd.DataFrame(data=data, columns=columns)

# savings_df.to_sql('savings', engine, index=False, if_exists='append')
#--------------------------------------------------
