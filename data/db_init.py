import psycopg2
import psycopg2.extras
import psycopg2.extensions
from datetime import datetime, timedelta
import json
import os
import faker
import random

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(__location__ + "/config.json", "r") as f:
    connectionString = json.load(f)["connectionString"]

connection_string = connectionString
cur: psycopg2.extras.DictCursor = None
conn: psycopg2.extensions.connection = None

def connect(credentials: dict[str, str] = None):
    global conn
    global cur
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

def close():
    cur.close()
    conn.close()

def inilize_db():
    cur.execute("CREATE TABLE IF NOT EXISTS ParentUsers (id SERIAL PRIMARY KEY, UserName VARCHAR(50) NOT NULL, Password VARCHAR(50) NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS ChildUsers (id SERIAL PRIMARY KEY, ParentID INTEGER NOT NULL, FOREIGN KEY (ParentID) REFERENCES ParentUsers(id), UserName VARCHAR(50) NOT NULL, Division VARCHAR(50) NOT NULL, loged_in BOOLEAN NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS LoginTimeTracker (id SERIAL PRIMARY KEY, ChildID INTEGER NOT NULL, LoginTime TIMESTAMP NOT NULL, LogoutTime TIMESTAMP, FOREIGN KEY (ChildID) REFERENCES ChildUsers(id));")
    cur.execute("CREATE TABLE IF NOT EXISTS Notes (id SERIAL PRIMARY KEY, ChildID INTEGER NOT NULL, Date TIMESTAMP NOT NULL, Note VARCHAR(1000) NOT NULL, is_staff BOOLEAN NOT NULL, FOREIGN KEY (ChildID) REFERENCES ChildUsers(id));")
    cur.execute("CREATE TABLE IF NOT EXISTS DivisionNotes (id SERIAL PRIMARY KEY, Date TIMESTAMP NOT NULL, Note VARCHAR(1000) NOT NULL, Division VARCHAR(50) NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS companyNotes (id SERIAL PRIMARY KEY, Date TIMESTAMP NOT NULL, Note VARCHAR(1000) NOT NULL);")
    conn.commit()

def create_test_data():

    divsion = ["Nature", "Technology", "Humanity"]
    fake = faker.Faker()
    cur.execute("INSERT INTO ParentUsers (UserName, Password) VALUES ('admin', 'password');")

    parent_password = "password"
    for i in range(10):
        parent_username = fake.name()
        cur.execute("INSERT INTO ParentUsers (UserName, Password) VALUES (%s, %s);", (parent_username, parent_password))
    conn.commit()
    for i in range(11):
        child_name = fake.name()
        _divison = random.choice(divsion)
        cur.execute("INSERT INTO ChildUsers (parentID, UserName, Division, loged_in) VALUES (%s, %s, %s, %s);", (i+1, child_name, _divison, False))
    for i in range(6):
        child_name = fake.name()
        _divison = random.choice(divsion)
        cur.execute("INSERT INTO ChildUsers (parentID, UserName, Division, loged_in) VALUES (%s, %s, %s, %s);", (i+1, child_name, _divison, True))
    conn.commit()
    for i in range(6):
        login_time = datetime.now()
        cur.execute("INSERT INTO LoginTimeTracker (ChildID, LoginTime) VALUES (%s, %s);", (11+i, login_time))
    conn.commit()

def drop_db():
    #Use DROP ... CASCADE to drop all objects that depend on the table, or use DROP ... RESTRICT to disallow dropping the table if any objects depend on it.
    cur.execute("DROP TABLE IF EXISTS LoginTimeTracker CASCADE;")
    cur.execute("DROP TABLE IF EXISTS ChildUsers CASCADE;")
    cur.execute("DROP TABLE IF EXISTS ParentUsers CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Notes CASCADE;")
    cur.execute("DROP TABLE IF EXISTS DivisionNotes CASCADE;")
    cur.execute("DROP TABLE IF EXISTS companyNotes CASCADE;")
    conn.commit()

if __name__ == "__main__":
    connect()
    drop_db()
    inilize_db()
    create_test_data()
    close()