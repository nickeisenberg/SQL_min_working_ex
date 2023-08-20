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
database = Create(base=base)

database.initialize(engine, no_parents=5, no_children=10)

# add some dependents after the fact

with engine.begin() as conn:
    children_df = pd.read_sql_query(
        db.text("""select * from children"""), engine
    )

columns = children_df.columns.values[1:]

parent1_id = [1, 1, 1]
parent2_id = [2, 2, 2]
first_name = ['nick', 'jack', 'jane']
last_name = ['eisenberg', 'johnson', 'godall']
same_residence = [True, True, False]
is_student = [False, True, False]
is_employed = [False, True, True]

data = np.vstack(
    [parent1_id, parent2_id, first_name, last_name, same_residence, is_student, is_employed]
).T

parent_df = pd.DataFrame(data=data, columns=columns)
parent_df.replace({'True': 1, 'False': 0}, inplace=True)

parent_df.to_sql('children', engine, index=False, if_exists='append')
