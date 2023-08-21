import sqlalchemy as db
from sqlalchemy.orm import declarative_base as Base
from parents_and_children.create import Create 
import numpy as np
import pandas as pd

# mysql
engine = db.create_engine(
    'mysql+pymysql://root:@127.0.0.1:3306/practice?unix_socket=/tmp/mysql.sock'
)

# sqlite
# path = '/Users/nickeisenberg/GitRepos/DataSets_local/test.db'
# path = './test.db'
# engine = db.create_engine(f'sqlite:///{path}')

# initialize the class and the database

base = Base()
database = Create(engine=engine, base=base)

database.initialize(no_parents=10, no_children=10)

# add some dependents after the fact
emp_df = pd.read_sql("""select * from employment""", engine)

emp_df.columns.values

columns = emp_df.columns.values[1:]

job = ['a', 'a']
salary = [100.01, 1011.0234]
start_date = ['1111', '1111']

data = np.vstack(
    [job, salary, start_date]
).T

emp_df = pd.DataFrame(data=data, columns=columns)

emp_df.to_sql('employment', engine, index=False, if_exists='append')
