from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import socket, Database, time, os
from functools import wraps
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


global username 
username = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "your_moms"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



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
    return render_template('menu.html', username=username)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def hello():
    global username
    if request.method == 'GET':
        notes = Database.get_notes_by_username(username)
        return render_template('notes.html', username = username, notes = notes)
    if request.method == 'POST':
        
        if(request.form.get('update')) == 'add':
            new_note = request.form['new_note']
            Database.add_note_by_user(username, new_note)
        else:
            note_to_delete = request.form.get('id')
            Database.delete_note_by_id(note_to_delete)

        notes = Database.get_notes_by_username(username)
        return render_template('notes.html', username = username, notes = notes)


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



# @app.route('/upload_file', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/pics', methods=['GET', 'POST'])
@login_required
def pics():
    if request.method == 'POST':
        if(request.form.get('update')) == 'delete':
            pic_to_delete = request.form.get('id')
            Database.delete_pic_by_id(pic_to_delete)

        if 'file' not in request.files:
            flash('No file part')
            print "###################1"
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filepath)
            Database.add_pic_by_user(username, filepath)
            # return redirect(url_for('pics',
            #                         filename=filename))
    pics = Database.get_pics_by_username(username)
    return render_template('pics.html', username = username, pics = pics)


def check_for_valid_user(username, password):
    return Database.check_login(username, password)


def add_user(username, password):
    Database.add_user(username, password)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3141, debug=True)




























