import os
import requests

from flask import (render_template, redirect, url_for, request, Blueprint, session)

from online_judge.helpers.session import login_required

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
            {'title': 'Problem 1', 'text': '<p>Create a program to double the text in a file.</p><p><strong>Input: </strong>1 2 3 4</p><p><strong>Output: </strong>11 22 33 44</p>', 'id': 'Problem1'},
        {'title': 'Problem 2', 'text': 'Problem 2', 'id': 'Problem2'},
        {'title': 'Problem 3', 'text': 'Problem 3', 'id': 'Problem3'}
    ]
    return problems

def run_tests(code, lang):
    response = requests.post('http://smartypants.me:3000/test',
                  headers={'Content-Type': 'application/json'},
                  json={'code': code, 'email': 'temp@abc.com', 'language': lang, 'question': 1})
    return response.text, 200


@home_page.route('/', methods=['GET'])
@login_required
def display_problem_list():
    return render_template('home.html', problems=get_problems(), accepted_languages=ALLOWED_EXTENSIONS, username=session['username'])

@home_page.route('/', methods=['POST'])
@login_required
def submit_solution():
    '''
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
    '''

    code = request.form['code']

    language = request.form['lang']

    return run_tests(code, language)

    #return redirect(url_for('.home_get')) 
