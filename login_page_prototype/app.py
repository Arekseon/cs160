from flask import Flask, render_template, request, redirect, url_for, session, flash
import socket, Database, time
from functools import wraps



global username 
username = ''

app = Flask(__name__)

app.secret_key = "your_moms"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    global username
    if request.method == 'GET':
        notes = Database.get_notes_by_username(username)
        return render_template('hello.html', username = username, notes = notes)
    if request.method == 'POST':
        
        if(request.form.get('update')) == 'add':
            new_note = request.form['new_note']
            Database.add_note_by_user(username, new_note)
        else:
            note_to_delete = request.form.get('id')
            Database.delete_note_by_id(note_to_delete)

        notes = Database.get_notes_by_username(username)
        return render_template('hello.html', username = username, notes = notes)


@app.route('/test_stuff', methods=['GET', 'POST'])
def test_stuff():
    return render_template('test_stuff.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        global username 
        username = request.form['username']


        login_check_passed = check_for_valid_user(username, request.form['password'])

        if login_check_passed:
            session['logged_in'] = True
            return redirect (url_for('index'))
        else: 
            error = 'Invalid user'
    return render_template('login.html', error=error)



@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        check = Database.check_if_user_exist(username)

        if not check:
            add_user(username, request.form['password'])
            return redirect (url_for('login'))
        else:
            error = "such user already exist"


    return render_template('register.html', error=error)

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))



def check_for_valid_user(username, password):
    return Database.check_login(username, password)


def add_user(username, password):
    Database.add_user(username, password)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3141, debug=True)




























