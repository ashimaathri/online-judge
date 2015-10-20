import json
from flask import (render_template, Blueprint, request, session, current_app, redirect, url_for)

from online_judge.db.user import User
from online_judge.helpers.session import redirect_if_authenticated

auth = Blueprint('auth', __name__)

def validate_form():
    username = request.form['username']
    password = request.form['password']
    error = None

    if not username:
        error = json.dumps({'error': 'Username absent'})

    if not password:
        error = json.dumps({'error': 'Password absent'})

    return username, password, error

@auth.route('/', methods=['GET'])
@redirect_if_authenticated
def display_login_form():
    return render_template('login_register.html')

@auth.route('/login', methods=['POST'])
def login():
    username, password, error = validate_form()

    if error:
        return error, 400
    
    if not User.exists(username):
        return json.dumps({'error': 'Invalid credentials'}), 400

    user = User(username)

    if user.verify(password):
        session['username'] = username
        try:
            return redirect(request.args['next'])
        except KeyError:
            return redirect(url_for('home_page.display_problem_list'))
    else:
        return json.dumps({'error': 'Invalid credentials'}), 400

@auth.route('/signup', methods=['POST'])
def signup():
    username, password, error = validate_form()

    if error:
        return error, 400

    if User.exists(username):
        return json.dumps({'error': 'Username exists'}), 400
    else:
        User(username, password).save()
        return json.dumps({'status': 'success'}), 200

@auth.route('/logout', methods=['GET'])
def logout():
    current_app.session_interface.store.remove({'sid': session.sid})
    session.clear()
    return redirect(url_for('.display_login_form'))
