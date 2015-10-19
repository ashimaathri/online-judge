from flask import (render_template, Blueprint, request, session)

from db.user import User

auth = Blueprint('auth', __name__)

def validate_form():
    username = request.form['username']
    password = request.form['password']
    error = None

    if not username:
        error = 'Username absent'

    if not password:
        error = 'Password absent', 400

    return username, password, error

@auth.route('/', methods=['GET'])
def display_login_form():
    return render_template('login_register.html', username=session.get('username'))

@auth.route('/login', methods=['POST'])
def login():
    username, password, error = validate_form()

    if error:
        return error, 400
    
    if not User.exists(username):
        return 'Invalid credentials', 400

    user = User(username)

    if user.verify(password):
        session['username'] = username
        return 'Login successful', 200
    else:
        return 'Invalid Credentials', 400

@auth.route('/signup', methods=['POST'])
def signup():
    username, password, error = validate_form()

    if error:
        return error, 400

    if User.exists(username):
        return 'Username exists', 400
    else:
        User(username, password).save()
        return 'New user {} created'.format(username), 200
