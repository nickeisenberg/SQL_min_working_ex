import faker
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import numpy as np

from creation.make_tables import (
    Mailing, Employment, Finances, Dependents
)

from creation.make_data import (
    savings_generator,
    salary_generator,
    startdate_generator,
    dependent_generator,
    SALARY_AVG, JOBS
)

fk = faker.Faker()

engine = db.create_engine(
    'mysql+pymysql://root:@127.0.0.1:3306/practice?unix_socket=/tmp/mysql.sock'
)

# add the rows
no_entries = 50
session  = sessionmaker(bind=engine)()
for i in range(no_entries):
    mailing = Mailing(
        fk.first_name(),
        fk.last_name(),
        fk.street_address(),
        fk.city(),
        fk.state(),
        fk.zipcode(),
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
        fk.bban(),
        savings_generator(SALARY_AVG[job]),
    )
    session.add(finances)
    num_dependents = dependent_generator()
    if num_dependents > 0:
        for dep in range(num_dependents):
            dependents = Dependents(
                policyholder_id=int(i + 1),
                first_name=fk.first_name(),
                last_name=fk.last_name(),
                same_residence=[False, True][np.random.binomial(1, .8)],
                is_student=[False, True][np.random.binomial(1, .8)],
                is_employed=[False, True][np.random.binomial(1, .6)]
            )
            session.add(dependents)
session.commit()


