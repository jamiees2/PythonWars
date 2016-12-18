from flask import Flask, redirect, render_template, url_for, request, session, make_response, jsonify
from pythonwars.models import db, User, Score
from pythonwars.util import is_logged_in, login_required, context_processor, get_user
from pythonwars.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import pythonwars.engine as engine
import pythonwars.engine.levels as levels

pythonwars = Flask(__name__)
pythonwars.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
pythonwars.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
pythonwars.secret_key = SECRET_KEY

db.init_app(pythonwars)

pythonwars.context_processor(context_processor)


@pythonwars.route('/')
def index():
    scores = Score.query.order_by(Score.score, Score.length).all()
    users = User.query.all()
    users = {user.id: user for user in users}
    scoreboard = {}
    for score in scores:
        if score.user_id not in scoreboard:
            scoreboard[score.user_id] = {"user": users[score.user_id], "total": (0, 0)}
        if score.level in scoreboard[score.user_id]:
            continue
        scoreboard[score.user_id][score.level] = (score.score, score.length)
        a, b = scoreboard[score.user_id]["total"]
        scoreboard[score.user_id]["total"] = (a + score.score, b + score.length)
    scoreboard = sorted(scoreboard.values(), key=lambda k: (k["total"][0], k["total"][1]))
    return render_template('index.html', data=scoreboard)


@pythonwars.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        print(username + ":" + password)

        user = User.query.filter_by(username=username).first()
        if user.checkPassword(password):
            session["user"] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="incorrect credentials")


@pythonwars.route('/logout')
@login_required
def logout():
    session.pop('user', '')
    return redirect(url_for('index'))


@pythonwars.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            userCheck = User.query.filter_by(username=username).first()
            if not userCheck:
                user = User(username, password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        return redirect(url_for('register'))


@pythonwars.route('/level', methods=['GET'])
@login_required
def dashboard():
    # TODO: find first board user hasn't completed?
    return redirect(url_for('level', id='1'))


@pythonwars.route('/level/<id>', methods=['GET'])
@login_required
def level(id):
    #highest = Score.query.filter_by(user=get_user(), level=id).orderBy(steps).first()
    #score=highest
    return render_template('dashboard.html', level=id, levels=sorted(levels.levels.keys()))


@pythonwars.route('/maze/<string:level>', methods=['GET'])
@login_required
def get_maze(level):
    out = {}
    try:
        data = levels.levels[level]()
        out = data["world"].get_data(hidden=data.get("mode", levels.MODE_REGULAR) == levels.MODE_INVISIBLE)
    except:
        out = {"error": True}
    return jsonify(out)


@pythonwars.route('/submit/<string:level>', methods=['POST'])
@login_required
def submit(level):
    code = request.form['data']
    print(code)
    out = engine.run_subprocess(code, level)
    print(out)
    if out['victory']:
        dupeCheck = Score.query.filter_by(user=get_user(), code=code, level=level).first()
        if not dupeCheck:
            length = len(code.replace(" ", ""))
            score = Score(get_user(), level, out['moves'], length, code, out['moves'])
            db.session.add(score)
            db.session.commit()
        else:
            out['results'] = "Duplicate Submission"
            out['success'] = False
    return jsonify(out)
