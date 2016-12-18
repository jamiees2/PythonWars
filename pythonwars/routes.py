from flask import Flask, redirect, render_template, url_for, request, session, jsonify
from pythonwars.models import db, User, Score
from pythonwars.util import login_required, context_processor, get_user
from pythonwars.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import pythonwars.engine as engine
import pythonwars.engine.levels as levels

# Initialize the flask app
pythonwars = Flask(__name__)

#  Configure the app
pythonwars.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
pythonwars.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
pythonwars.secret_key = SECRET_KEY

# Initialize the database
db.init_app(pythonwars)

# Assign the context processor
pythonwars.context_processor(context_processor)


@pythonwars.route('/')
def index():
    # Fetch all scores from the database
    scores = Score.query.order_by(Score.score, Score.length).all()

    # Fetch all the users
    users = User.query.all()
    users = {user.id: user for user in users}

    # Populate the scoreboard
    scoreboard = {}
    for score in scores:
        # Check if the user is already in the scoreboard
        if score.user_id not in scoreboard:
            scoreboard[score.user_id] = {"user": users[score.user_id], "total": (0, 0), "total_levels": 0}

        # Make sure the current level for this user isn't already on the scoreboard
        if score.level in scoreboard[score.user_id]:
            continue

        # Assign the score of the current level
        scoreboard[score.user_id][score.level] = (score.score, score.length)

        # Fetch current total score of the user
        a, b = scoreboard[score.user_id]["total"]

        # Add to the total score
        scoreboard[score.user_id]["total"] = (a + score.score, b + score.length)
        scoreboard[score.user_id]["total_levels"] += 1

    # Sort the scoreboard first after total amount of levels completed in decreasing order, then by total score proceeded by the total time.
    scoreboard = sorted(scoreboard.values(), key=lambda k: (-k["total_levels"], k["total"][0], k["total"][1]))

    # Render the index template with the scoreboard data
    return render_template('index.html', data=scoreboard, levels=levels.level_list)


@pythonwars.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # If it's a get request we can just display the login page
        return render_template('login.html')
    elif request.method == 'POST':
        # If it's a post request we have to handle the login data

        # Extract the credentials from the form
        username = request.form["username"]
        password = request.form["password"]

        # Fetch the queried user
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and whether the password matched
        if user and user.checkPassword(password):
            # Activate a session with the current connection
            session["user"] = user.id

            # Display the dashboard
            return redirect(url_for('dashboard'))
        else:
            # Return an error
            return render_template('login.html', error="incorrect credentials")


@pythonwars.route('/logout')
@login_required
def logout():
    # Remove the session of the current connection
    session.pop('user', '')

    # Redirect back to the index
    return redirect(url_for('index'))


@pythonwars.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Display the registration form
        return render_template('register.html')
    elif request.method == 'POST':
        # Extract the registration data
        username = request.form["username"]
        password = request.form["password"]

        # Make sure both the username and password were entered
        if username and password:
            # Check if someone already has registered with that username
            userCheck = User.query.filter_by(username=username).first()
            if not userCheck:
                # If no user with that username was found we register the new user

                # Create a new user object from the user model
                user = User(username, password)

                # Add the user to the current database session
                db.session.add(user)

                # Commit the transaction to the database
                db.session.commit()

                # The user can now login with the credentials so he is redirected to the login page
                return redirect(url_for('login'))

        # Otherwise we just redirect back to the registration form
        return redirect(url_for('register'))


@pythonwars.route('/level', methods=['GET'])
@login_required
def dashboard():
    # TODO: find first board user hasn't completed?
    return redirect(url_for('level', id='1'))


@pythonwars.route('/level/<id>', methods=['GET'])
@login_required
def level(id):
    return render_template('dashboard.html', level=id, level_list=levels.level_list, levels=levels.levels)


@pythonwars.route('/maze/<string:level>', methods=['GET'])
@login_required
def get_maze(level):
    out = {}
    try:
        # Fetch the level data
        data = levels.levels[level]()

        # Get maze info and pass in the level mode, whether it's a hidden level or not.
        out = data["world"].get_data(hidden=data.get("mode", levels.MODE_REGULAR) == levels.MODE_INVISIBLE)
    except:
        # No level with the given id was found
        out = {"error": True}

    # Return the result in JSON
    return jsonify(out)


@pythonwars.route('/submit/<string:level>', methods=['POST'])
@login_required
def submit(level):
    # Extract the code from the form
    code = request.form['data']

    # Excute the code in the bot engine
    out = engine.run_subprocess(code, level)

    # Check if the bot finished the level
    if out['victory']:
        # Make sure that the level hasn't been finished with the same code before
        dupeCheck = Score.query.filter_by(user=get_user(), code=code, level=level).first()
        if not dupeCheck:
            # Get the number of characters in solution
            length = len(code.replace(" ", ""))

            # Assign the score
            score = Score(get_user(), level, out['moves'], length, code, out['moves'])

            # Add the score to the database
            db.session.add(score)
            db.session.commit()
        else:
            # Return an error stating a duplicate submission was recieved
            out['results'] = "Duplicate Submission"
            out['success'] = False

    # Return a JSON response containing the maze along with the robot's moves
    return jsonify(out)
