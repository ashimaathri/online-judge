from functools import wraps
from flask import session, url_for, request, redirect

def is_authenticated():
    return 'username' in session

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_authenticated():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.display_login_form') + '?next={}'.format(request.path))
    return wrapper

def redirect_if_authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_authenticated():
            try:
                return redirect(request.args['next'])
            except KeyError:
                return redirect(url_for('home_page.display_problem_list'))
        else:
            return f(*args, **kwargs)
    return wrapper
