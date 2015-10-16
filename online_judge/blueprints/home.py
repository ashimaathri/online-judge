import os

from flask import (render_template, redirect, url_for, request, Blueprint)

ALLOWED_EXTENSIONS = ['c', 'py', 'php']
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER='{}/submissions'.format(APP_ROOT)

home_page = Blueprint('home_page', __name__, url_prefix='/home')

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def secure_filename(filename):
    return filename

def get_problems():
    problems = [
        {'title': 'Problem 1', 'text': 'Problem 1', 'id': 'Problem1'},
        {'title': 'Problem 2', 'text': 'Problem 2', 'id': 'Problem2'},
        {'title': 'Problem 3', 'text': 'Problem 3', 'id': 'Problem3'}
    ]
    return problems

def run_tests(filename):
    # Make a curl request to API
    pass

@home_page.route('/', methods=['GET'])
def home_get():
    return render_template('home.html', problems=get_problems(), accepted_languages=ALLOWED_EXTENSIONS)

@home_page.route('/', methods=['POST'])
def home_post():
    try:
        submission = request.files['submission']
    except KeyError:
        return 'Empty File', 400

    if not submission.filename:
        return 'Empty File', 400

    if not allowed_files(submission.filename):
        return 'Incorrect file', 400

    filename = secure_filename(submission.filename)

    submission.save(os.path.join(UPLOAD_FOLDER, filename))

    run_tests(os.path.join(UPLOAD_FOLDER, filename))

    return redirect(url_for('.home_get')) 
