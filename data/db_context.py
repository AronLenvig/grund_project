import psycopg2
import psycopg2.extras
import psycopg2.extensions
from datetime import datetime, timedelta
import json
import os



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

def get_childrens_in_division(division: str) -> list[tuple[int, str]]:
    cur.execute("SELECT id, username FROM ChildUsers WHERE Division = %s;", (division,))
    children = cur.fetchall()
    return children

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

def get_notes_day(child_id: int, day: int) -> list[tuple[datetime, str, bool]]:
    cur.execute("SELECT Date, Note, is_staff FROM Notes WHERE ChildID = %s;", (child_id,))
    # do the day calc after the query, so that the query is only executed once
    notes = cur.fetchall()
    notes = [(date, note, is_staff) for date, note, is_staff in notes if date.date() == (datetime.now() + timedelta(days=day)).date()]
    return notes

def get_divison_notes_day(division: str, day: int) -> list[tuple[datetime, str]]:
    cur.execute("SELECT Date, Note FROM DivisionNotes WHERE Division = %s;", (division,))
    # do the day calc after the query, so that the query is only executed once
    notes = cur.fetchall()
    notes = [(date, note) for date, note in notes if date.date() == (datetime.now() + timedelta(days=day)).date()]
    return notes

def get_company_notes_day(day: int) -> list[tuple[datetime, str]]:
    cur.execute("SELECT Date, Note FROM companyNotes;")
    # do the day calc after the query, so that the query is only executed once
    notes = cur.fetchall()
    notes = [(date, note) for date, note in notes if date.date() == (datetime.now() + timedelta(days=day)).date()]
    return notes

def add_note_to_child(child_id: int, note: str, is_staff: bool):
    cur.execute("INSERT INTO Notes (ChildID, Date, Note, is_staff) VALUES (%s, %s, %s, %s);", (child_id, datetime.now(), note, is_staff))
    conn.commit()

def add_note_to_division(division: str, note: str):
    cur.execute("INSERT INTO DivisionNotes (Date, Note, Division) VALUES (%s, %s, %s);", (datetime.now(), note, division))
    conn.commit()

def add_note_to_company(note: str):
    cur.execute("INSERT INTO companyNotes (Date, Note) VALUES (%s, %s);", (datetime.now(), note))
    conn.commit()

def add_login_time(child_id: int, login_time: datetime):
    # verify that child is not already logged in
    if is_child_logged_in(child_id):
        print("Child is already logged in")
        return False
    cur.execute("UPDATE ChildUsers SET loged_in = %s WHERE id = %s;", (True, child_id))
    cur.execute("INSERT INTO LoginTimeTracker (ChildID, LoginTime) VALUES (%s, %s);", (child_id, login_time))
    conn.commit()
    return True

def add_logout_time(child_id: int, logout_time: datetime):
    # verify that child is logged in
    if not is_child_logged_in(child_id):
        print("Child is already logged out")
        return False
    cur.execute("UPDATE ChildUsers SET loged_in = %s WHERE id = %s;", (False, child_id))
    cur.execute("UPDATE LoginTimeTracker SET LogoutTime = %s WHERE ChildID = %s AND LogoutTime IS NULL;", (logout_time, child_id))
    conn.commit()
    return True

def get_login_time_in_week(child_id: int, week: int = 0) -> list[tuple[datetime, datetime]]:
    cur.execute("SELECT LoginTime, LogoutTime FROM LoginTimeTracker WHERE ChildID = %s;", (child_id,))
    login_times = cur.fetchall()
    #fix monday is the first day of the week and sunday is the last day of the week
    if week == 0:
        login_times = [(login_time, logout_time) for login_time, logout_time in login_times if login_time.date() >= (datetime.now() - timedelta(days=datetime.now().weekday())).date() and login_time.date() <= (datetime.now() + timedelta(days=6 - datetime.now().weekday())).date()]
    elif week > 0:
        login_times = [(login_time, logout_time) for login_time, logout_time in login_times if login_time.date() >= (datetime.now() + timedelta(days=7 * week - datetime.now().weekday())).date() and login_time.date() <= (datetime.now() + timedelta(days=7 * week + 6 - datetime.now().weekday())).date()]
    else:
        login_times = [(login_time, logout_time) for login_time, logout_time in login_times if login_time.date() >= (datetime.now() + timedelta(days=7 * week - datetime.now().weekday())).date() and login_time.date() <= (datetime.now() + timedelta(days=7 * week + 6 - datetime.now().weekday())).date()]
    return login_times

        

def update_parent_password(parent_id: int, parent_password: str):
    cur.execute("UPDATE ParentUsers SET Password = %s WHERE id = %s;", (parent_password, parent_id))
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
    pass
