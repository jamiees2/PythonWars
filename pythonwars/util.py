import functools
from flask import redirect, url_for, request, session, current_app as pythonwars
from pythonwars.models import User
def is_logged_in():
    # Check the session exists
    return 'user' in session

def get_user():
    # Make sure the user is logged in
    if not is_logged_in():
        return None
    # Query for the user current user
    user = User.query.filter(User.id == session["user"]).first()
    return user

def login_required(f):
    # Decoration function that makes sure that the user is logged in
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Check if the user is logged in
        if not is_logged_in():
            # Redirect the user to the login page
            return redirect(url_for('login', next=request.script_root + request.path))
        # Otherwise continue to the original route
        return f(*args, **kwargs)
    return decorated

def context_processor():
    # Get the current user
    user = get_user()

    # Load the user into the context processor so we can always interact with the user object
    return dict(
        user=user
    )
