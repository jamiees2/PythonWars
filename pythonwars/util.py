import functools
from flask import redirect, url_for, request, session, current_app as pythonwars
from pythonwars.models import User
def is_logged_in():
    return 'user' in session

def get_user():
    if not is_logged_in():
        return None
    user = User.query.filter(User.id == session["user"]).first()
    return user

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login', next=request.script_root + request.path))
        return f(*args, **kwargs)
    return decorated

def context_processor():
    user = get_user()
    return dict(
        user=user
    )
