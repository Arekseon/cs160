from flask import Flask, render_template, request, redirect, url_for, session, flash
import socket
from functools import wraps



global username 
username = ''

app = Flask(__name__)

app.secret_key = "your_mom"


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
    return render_template('hello.html', username = username)


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
        add_user(request.form['username'], request.form['password'])
        return redirect (url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))



def check_for_valid_user(username, password):
    logged = False
    f = open('users.txt', 'r')
    for line in f:
        try:
            pair = line.split()
            valid_username =  pair[0]
            valid_password = pair[2]
            if username == valid_username and password == valid_password:
                logged = True
        except Exception, e:
            print ''
        
    return logged

def add_user(username, password):
    string_to_add = "\n" + username + " - " + password
    with open("users.txt", "a") as f:
        f.write(string_to_add)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3141, debug=True)




























