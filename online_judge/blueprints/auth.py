from flask import (render_template, Blueprint)

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def display_login_form():
    return render_template('login_register.html')

@auth.route('/login', methods=['POST'])
def login():
    return '', 200

@auth.route('/signup', methods=['POST'])
def signup():
    return '', 200
