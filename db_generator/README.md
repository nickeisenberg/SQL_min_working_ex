## Current database generators
1. parents_and_children

## How to use
* First clone or fork the repo onto your machine.
* To create the database, you first need to create an engine.
See [this link](https://docs.sqlalchemy.org/en/20/core/engines.html) for
information on engines. There is also a function in the `utils.py` folder that
will create the engine for you. This function should work with postgresql, but
I have only tested it for mysql. If you want to use sqlite as you database,
the engine simply becomes `sqlalchemy.create_engine('sqlite:///<path_to_db>')`.
* After creating the engine, open a python script and run the following 
(the following is for mysql and the parents_and_children generator):

```python
import sqlalchemy as db
from utils import engine_generator
from parents_and_children.create import Create
from sqlalchemy.orm import declarative_base as Base

# mysql
engine = engine_generator(
    dialect='mysql', 
    driver='pymysql', 
    username='root', 
    host='127.0.0.1',
    port='3306',
    db='practice',
    unix_socket='/tmp/mysql.sock'
)

# sqlite
path = "<path_to_where_you_want_you_sqlite.db_file>"
engine = db.create_engine(f'sqlite:///{path}')

base = Base()
database = Create(engine=engine, base=base)
database.initialize(
        no_jobs=5,
        include_unemployed=True,
        with_entries=True,
        drop_db_if_exists=True,
        no_parents=5,
        no_children=10
    )
```

* The database is now generated. As a simple test, you can run the following:
```python
import pandas as pd

pd.read_sql("""select * from employment""", engine)
```

* Now use any database IDE to run queries. There are also some practice 
questions listed in each of the database generator subdirectories that 
you can use for practice.
