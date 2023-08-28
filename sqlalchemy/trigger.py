import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base, validates
from sqlalchemy_utils import drop_database, create_database, database_exists
from sqlalchemy import event, DDL, ForeignKey


db_name = 'trigger'
db_type = 'mysql'
device = 'pymysql'
user = 'root'
host = '127.0.0.1'
port = '3306'
sock = '/tmp/mysql.sock'
engine = db.create_engine(
    f"{db_type}+{device}://{user}:@{host}:{port}/{db_name}?unix_socket={sock}"
)

if database_exists(engine.url):
    drop_database(engine.url)
if not database_exists(engine.url):
    create_database(engine.url)

base = declarative_base()

class Transactions(base):
    __tablename__ = 'trans'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    item = db.Column(db.String(20))
    action = db.Column(db.Float())
    no_units = db.Column(db.Float())
    def __init__(self, item, action, no_units):
        self.id = id
        self.item = item
        self.action = action
        self.no_units = no_units


class Inventory(base):
    __tablename__ = 'inv'
    item = db.Column(
        db.String(20), 
        primary_key=True, 
    )
    inv = db.Column(db.Integer())
    def __init__(self, item, inv):
        self.item = item
        self.inv = inv

base.metadata.create_all(bind=engine)




