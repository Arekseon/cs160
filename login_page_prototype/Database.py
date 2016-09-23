import sqlite3, datetime

global db_name_name
db_name_name = 'test_db.db'


def add_user(username, password):

    new_id = get_max_id("uuid","USERS") + 1
    current_time = str(datetime.datetime.now().time())
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO USERS (time, username, password, UUID) VALUES (?,?,?,?)
        ''', (current_time, username, password, new_id))
    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT password FROM USERS WHERE username=:input_username 
        ''', {"input_username": username})
    conn.commit()
    result = cursor.fetchone()
    conn.commit()
    conn.close()

    if result == None:
        return False

    if password == result[0]:
        return True
    else:   
        return False   


def check_if_user_exist(username):

    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT password FROM USERS WHERE username=:input_username 
        ''', {"input_username": username})
    conn.commit()
    result = cursor.fetchone()
    conn.commit()
    conn.close()

    return (not result==None)

def get_uuid_by_username(username):
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT UUID FROM USERS WHERE username=:input_username 
        ''', {"input_username": username})
    conn.commit()
    result = cursor.fetchone()
    conn.close()
    if result == None:
        return -1
    else:
        return result[0]


def add_note_by_user(username, note):
    add_note_by_uuid(get_uuid_by_username(username), note)


def add_note_by_uuid(uuid, note):
    new_id = get_max_id("note_id","NOTES") + 1
    current_time = str(datetime.datetime.now().time())
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO NOTES (time, user_id, note, note_id) VALUES (?,?,?,?)
        ''', (current_time, uuid, note, new_id))
    conn.commit()
    conn.close()

def get_row_count(table):
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()
    query = "SELECT COUNT(*) from " + table
    cursor.execute(query)
    result=cursor.fetchone()
    conn.close()
    return result[0]

def get_notes_by_username(username):
    uuid = get_uuid_by_username(username)
    return get_notes_by_uuid(get_uuid_by_username(username))

def get_notes_by_uuid(uuid):
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM NOTES WHERE user_id=:input
        ''', {"input": uuid})
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    if result == None:
        return -1
    else:
        return result


def get_max_id(id, table):
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()
    query = "SELECT MAX("+ id +") from " + table
    cursor.execute(query)
    result=cursor.fetchone()
    conn.close()
    if result[0] == None:
        return -1
    else:
        return result[0]

def delete_note_by_id(note_id):
    conn = sqlite3.connect(db_name_name)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM NOTES WHERE note_id=:input
        ''', {"input": note_id})
    conn.commit()
    conn.close()



