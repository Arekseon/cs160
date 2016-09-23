import sqlite3, os


try:
    os.remove('test_db.db')
except OSError:
    pass

conn = sqlite3.connect('test_db.db')
c = conn.cursor()

c.execute('''CREATE TABLE USERS
             (time text, username text, password text, UUID int)''')

#for now
c.execute('''CREATE TABLE NOTES
             (time text, user_id int, note text, note_id int)''')


conn.commit()
