import psycopg2
import psycopg2.extras
import psycopg2.extensions
from datetime import datetime, timedelta

connection_string = "dbname=grund_project_database user=postgres password=EgElskiPython2022 host=localhost port=5432"
cur: psycopg2.extras.DictCursor = None
conn: psycopg2.extensions.connection = None

def connect(credentials: dict[str, str] = None):

    # if not valid(credentials):
    #     return False
    
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
    cur.execute("CREATE TABLE IF NOT EXISTS Notes (id SERIAL PRIMARY KEY, ChildID INTEGER NOT NULL, Date TIMESTAMP NOT NULL, Note VARCHAR(1000) NOT NULL, FOREIGN KEY (ChildID) REFERENCES ChildUsers(id));")
    conn.commit()

def create_test_data():
    for i in range(10):
        parent_username = f"parent{i}"
        parent_password = f"password{i}"
        cur.execute("INSERT INTO ParentUsers (UserName, Password) VALUES (%s, %s);", (parent_username, parent_password))
    conn.commit()
    for i in range(10):
        child_name = f"child{i}"
        cur.execute("INSERT INTO ChildUsers (parentID, UserName, Division, loged_in) VALUES (%s, %s, %s, %s);", (i+1, child_name, "Nature", False))
    for i in range(5):
        child_name = f"child{i}{i}"
        cur.execute("INSERT INTO ChildUsers (parentID, UserName, Division, loged_in) VALUES (%s, %s, %s, %s);", (i+1, child_name, "Nature", True))
    conn.commit()
    for i in range(5):
        login_time = datetime.now()
        cur.execute("INSERT INTO LoginTimeTracker (ChildID, LoginTime) VALUES (%s, %s);", (11+i, login_time))
    conn.commit()

def drop_db():
    #Use DROP ... CASCADE to drop all objects that depend on the table, or use DROP ... RESTRICT to disallow dropping the table if any objects depend on it.
    cur.execute("DROP TABLE IF EXISTS LoginTimeTracker CASCADE;")
    cur.execute("DROP TABLE IF EXISTS ChildUsers CASCADE;")
    cur.execute("DROP TABLE IF EXISTS ParentUsers CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Notes CASCADE;")
    conn.commit()

def get_division(child_id: int) -> str:
    cur.execute("SELECT Division FROM ChildUsers WHERE id = %s;", (child_id,))
    division = cur.fetchone()[0]
    return division

def get_childrens(parent_id: int) -> list[tuple[int, str]]:
    cur.execute("SELECT id, username FROM ChildUsers WHERE ParentID = %s;", (parent_id,))
    children = cur.fetchall()
    return children

def is_child_logged_in(child_id: int) -> bool:
    cur.execute("SELECT loged_in FROM ChildUsers WHERE id = %s;", (child_id,))
    is_logged_in = cur.fetchone()[0]
    return bool(is_logged_in)

def add_note_to_child(child_id: int, note: str):
    cur.execute("INSERT INTO Notes (ChildID, Date, Note) VALUES (%s, %s, %s);", (child_id, datetime.now(), note))
    conn.commit()

def get_notes_day(child_id: int, day: int) -> list[tuple[datetime, str]]:
    """
    Returns a list of tuples with the date and the note for the given child on the given day.
    example if day = 0, it will return all notes for the current day.
    example if day = 1, it will return all notes for the next day.
    example if day = -1, it will return all notes for the previous day."""

    cur.execute("SELECT Date, Note FROM Notes WHERE ChildID = %s;", (child_id,))
    # do the day calc after the query, so that the query is only executed once
    notes = cur.fetchall()
    notes = [(date, note) for date, note in notes if date.date() == (datetime.now() + timedelta(days=day)).date()]
    return notes


def add_child(parent_id: int, child_username: str, child_division: str):
    cur.execute("INSERT INTO ChildUsers (UserName, ParentID, Division, loged_in) VALUES (%s, %s, %s, %s);", (child_username, parent_id, child_division, False))
    conn.commit()

def add_parent(parent_username: str, parent_password: str):
    cur.execute("INSERT INTO ParentUsers (UserName, Password) VALUES (%s, %s);", (parent_username, parent_password))
    conn.commit()

def add_login_time(child_id: int, login_time: datetime):
    # verify that child is not already logged in
    if is_child_logged_in(child_id):
        print("Child is already logged in")
        return False
    cur.execute("UPDATE ChildUsers SET loged_in = %s WHERE id = %s;", (True, child_id))
    cur.execute("INSERT INTO LoginTimeTracker (ChildID, LoginTime) VALUES (%s, %s);", (child_id, login_time))
    conn.commit()

def add_logout_time(child_id: int, logout_time: datetime):
    # verify that child is logged in
    if not is_child_logged_in(child_id):
        print("Child is already logged out")
        return False
    cur.execute("UPDATE ChildUsers SET loged_in = %s WHERE id = %s;", (False, child_id))
    cur.execute("UPDATE LoginTimeTracker SET LogoutTime = %s WHERE ChildID = %s AND LogoutTime IS NULL;", (logout_time, child_id))
    conn.commit()

def update_child(child_id: int, child_username: str):
    cur.execute("UPDATE ChildUsers SET UserName = %s WHERE id = %s;", (child_username, child_id))
    conn.commit()

def update_parent_password(parent_id: int, parent_password: str):
    cur.execute("UPDATE ParentUsers SET Password = %s WHERE id = %s;", (parent_password, parent_id))
    conn.commit()

def delete_child(child_id: int):
    cur.execute("DELETE FROM ChildUsers WHERE id = %s;", (child_id))
    conn.commit()

def delete_parent(parent_id: int):
    parent_children = get_childrens(parent_id)
    for child in parent_children:
        delete_child(child[0])
    cur.execute("DELETE FROM ParentUsers WHERE id = %s;", (parent_id))
    conn.commit()

def verify_login(username: str, password: str) -> bool:
    cur.execute("SELECT * FROM ParentUsers WHERE UserName = %s AND Password = %s;", (username, password))
    user = cur.fetchone()
    if user:
        return True
    else:
        return False
    
def get_parent_id(username: str, password: str) -> int:
    cur.execute("SELECT id FROM ParentUsers WHERE UserName = %s AND Password = %s;", (username, password))
    parent_id = cur.fetchone()
    return parent_id[0]
    
if __name__ == "__main__":
    connect()
    # add_note_to_child(1, "test")
    print(get_notes_day(1, 0))
    close()
