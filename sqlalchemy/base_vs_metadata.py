import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import declarative_base as Base

engine = db.create_engine(
    "mysql+pymysql://root:@127.0.0.1:3306/_temp_?unix_socket=/tmp/mysql.sock"
)

if database_exists(engine.url):
    drop_database(engine.url) 

if not database_exists(engine.url):
    create_database(engine.url) 

base = Base()
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

base.metadata.sorted_tables

base.metadata.create_all(bind=engine)

#--------------------------------------------------
meta = db.MetaData()

def User1(metadata):
    user = db.Table(
        "user1",
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

user1 = User1(meta)
user2 = User2(meta)

meta.sorted_tables

meta.create_all(bind=engine)

# base is uneeded. but you can still use it
base = Base(metadata=meta)
base.metadata.create_all(bind=engine)
#--------------------------------------------------

class Columns:

    @staticmethod 
    def user_id():
        return db.Column("user_id", db.Integer, primary_key=True)
    
    @staticmethod 
    def user_name(name, length):
       return db.Column(name, db.String(length), nullable=False)
    
    @staticmethod 
    def mail():
        return db.Column("email_address", db.String(60))
    
    @staticmethod 
    def nickname():
        return db.Column("nickname", db.String(50), nullable=False)

Columns.user_name('username', 20)

user_name = columns.user_name('username', 20)
