## Current database generators
1. parents_and_children

## How to use
* The best way to use the repo would be to clone or fork it onto your machine
* You could either clone it the directory where your python looks for libraries
or just append your path with `sys.path.append` when you want to call the
classes to build the databases.
* To create the database, you first need to create an engine.
See [this link](https://docs.sqlalchemy.org/en/20/core/engines.html) for
information on engines. There is also a function in the `utils.py` folder that
will create the engine for you. This function should work with postgresql but
I ahve only tested it for mysql. If you want to use sqlite as you database,
the engine simply becomes `sqlalchemy.create_engine('sqlite:///<path_to_db>')`.
* After creating the engine, open a python script and run the following 
(the following is for mysql and the parents_and_children generator):

```python
from utils import engine_generator
from parents_and_children.create import Create
from sqlalchemy.orm import declarative_base as Base

engine = engine_generator(
    dialect='mysql', 
    driver='pymysql', 
    username='root', 
    host='127.0.0.1',
    port='3306',
    db='practice',
    unix_socket='/tmp/mysql.sock'
)

base = Base()
database = Create(engine=engine, base=base)
database.initialize(no_parents=10, no_children=5)
```

* The database is now generated. As a simple test, you can run the following:c
```python
import pandas as pd

pd.read_sql("""select * from employment""", engine)
```

* Now use any database IDE. There are also some practice questions listed in
each of the database generator subdirectories that you can use for practice.







