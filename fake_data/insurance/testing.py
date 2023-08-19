import sqlalchemy as db
from insurance.create import Create 
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
database = Create()

database.initialize(engine, 5)

# add some dependents after the fact

with engine.begin() as conn:
    dependent_df = pd.read_sql_query(
        db.text("""select * from dependents"""), engine
    )

dependent_df.head()

columns=[
    'policyholder_id',
    'first_name',
    'last_name',
    'same_residence',
    'is_student',
    'is_employed'
]

policyholder_id = [1, 1, 1]
first_name = ['nick', 'jack', 'jane']
last_name = ['eisenberg', 'johnson', 'godall']
same_residence = [True, True, False]
is_student = [False, True, False]
is_employed = [False, True, True]

data = np.vstack(
    [policyholder_id, first_name, last_name, same_residence, is_student, is_employed]
).T

dependent_df = pd.DataFrame(data=data, columns=columns)
dependent_df.replace({'True': 1, 'False': 0}, inplace=True)

dependent_df.to_sql('dependents', engine, index=False, if_exists='append')
