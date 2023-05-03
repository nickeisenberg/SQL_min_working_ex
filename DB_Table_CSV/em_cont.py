import pandas as pd
import numpy as np
import pymysql
import sqlalchemy as alc

names = pd.Series(
    ['jack' , 'Rebecca'],
    name='name'
)
numbers = pd.Series(
    [7024354444, 4321112121],
    name='number'
)
relation = pd.Series(
    ['friend', 'wife'],
    name='relation'
)

em_cont_df = pd.DataFrame(
    data=[names, numbers, relation]
).T

em_cont_df.to_csv('em_cont.csv')

# Open a connection to the database
connection = pymysql.connect(
    host='test-server-azure.mysql.database.azure.com',
    user='nickeisenberg',
    password='',
)

# We can view tables from the database
cursor = connection.cursor()
_ = cursor.execute(
    "SELECT * FROM person_info.contact"
)
for i in cursor.fetchall():
    print(i)

# Now lets insert the em_cont_df into the emergency_contact
# table in the database.
# We can also create the table as well if it does not already exist

sql_code = "DROP TABLE IF EXISTS person_info.emergency_contact; "
_ = connection.cursor().execute(sql_code)

sql_code = "CREATE TABLE person_info.emergency_contact( "
sql_code += "person_id INT AUTO_INCREMENT PRIMARY KEY, "
sql_code += "name VARCHAR(255) NOT NULL, "
sql_code += "number VARCHAR(15) NOT NULL, "
sql_code += "relation VARCHAR(200) DEFAULT NULL); "
_ = connection.cursor().execute(sql_code)

cols = ",".join(em_cont_df.columns.values)
for row in em_cont_df.values:
    sql_code = f"INSERT INTO person_info.emergency_contact({cols}) "
    sql_code += "VALUES "
    sql_code += f"{tuple(row)}"
    _ = connection.cursor().execute(sql_code)
connection.commit()

# Instead of inserting line by line, we can insert the whole dataframe
# using sqlalchemy.

host = "test-server-azure.mysql.database.azure.com"
schema = "person_info"
port = 3306
user = "nickeisenberg"
p_w = ""
cnx = alc.create_engine(f'mysql+pymysql://{user}:{p_w}@{host}:{port}/{schema}', echo=False)

sql_code = "DROP TABLE IF EXISTS person_info.emergency_contact; "
_ = connection.cursor().execute(sql_code)

sql_code = "CREATE TABLE person_info.emergency_contact( "
sql_code += "person_id INT AUTO_INCREMENT PRIMARY KEY, "
sql_code += "name VARCHAR(255) NOT NULL, "
sql_code += "number VARCHAR(15) NOT NULL, "
sql_code += "relation VARCHAR(200) DEFAULT NULL); "
_ = connection.cursor().execute(sql_code)

em_cont_df.to_sql(
    name='emergency_contact',
    con=cnx,
    if_exists='append',
    index=False
)

