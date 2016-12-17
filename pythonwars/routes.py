from flask import Flask, redirect, render_template, url_for, request, session, make_response, jsonify
from pythonwars.models import db, User
from pythonwars.util import is_logged_in, login_required, context_processor
from pythonwars.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import pythonwars.engine as engine
import pythonwars.engine.levels as levels
import os

pythonwars = Flask(__name__)
pythonwars.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
pythonwars.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
pythonwars.secret_key = SECRET_KEY

db.init_app(pythonwars)

pythonwars.context_processor(context_processor)


@pythonwars.route('/')
def index():
    return render_template('index.html')


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
    return redirect(url_for('level',id=1))

@pythonwars.route('/level/<id>', methods=['GET'])
@login_required
def level(id):
    return render_template('dashboard.html', level=id)

@pythonwars.route('/maze/<string:level>', methods=['GET'])
@login_required
def get_maze(level):
    data = levels.levels[level]()
    out =  data["world"].get_data()
    return jsonify(out)

@pythonwars.route('/submit', methods=['POST'])
@login_required
def submit():
    code = request.form['data']
    print(code)
    out = engine.run(code, "level1")
    return jsonify(out)
