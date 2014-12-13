# imports
import functools
import sqlite3
import map_graph
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, views, current_app
from werkzeug.security import generate_password_hash, \
    check_password_hash
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask.ext.wtf.html5 import EmailField
from contextlib import closing
from copy import copy
from map_graph import stringify, string_to_graph, decision_at_node_N, distance
from json import dumps
from math import cos , sin , acos, asin, pi


# confifuration instructions
DATABASE = 'app.db'
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'
# temporary test database
users = {'test1@gmail.com': '1'}
# application initiation
app = Flask(__name__)
app.config.from_object(__name__)


def ssl_required(fn):
    """
    Decorator for https redirection in inscure http
    pages such as login and sigup
    """
    @functools.wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                print 1
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))
        return fn(*args, **kwargs)

    return decorated_view


###############################################################################
#                        NON URL CLASSES                                      #
###############################################################################


class RegistrationForm(Form):
    """
    Registration form validation class
    """
    email = EmailField('email', [
        validators.Length(min=1, max=35),
        validators.Required()
        ])
    addr = TextField('addr', [
        validators.Length(min=1, max=35),
        validators.Required()
        ])
    key = TextField('key', [
        validators.Required(),
        validators.EqualTo('key2', message='Passwords must match')
        ])
    key2 = TextField('key2')


class User(object):
    """
    Password salting class
    """

    def __init__(self, username, password, addr=''):
        self.username = username
        self.set_password(password)
        self.addr = addr

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


###############################################################################
#                        END                                                  #
###############################################################################


class Login(views.MethodView):
    @ssl_required
    def get(self):
        # small db check
        print "####################"
        cur = get_db().cursor()
        cur.execute(" SELECT * FROM user;")
        print cur.fetchall()
        print "####################"
        redirect(request.url.replace("http://", "https://"))
        return render_template('login.html')

    @ssl_required
    def post(self):
        if 'logout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))
        username = request.form['email']
        passwd = request.form['key']
        user = User(username, passwd)
        query = """SELECT user.password
                   FROM user
                   WHERE user.user = ?;
                """
        cur = get_db().cursor()
        print user.username
        cur.execute(query, (user.username,))
        result = cur.fetchall()
        print len(result) > 0
        if len(result) > 0:
            user.pw_hash = result[0][0]
            if user.check_password(passwd):
                session['logged_in'] = True
                session['username'] = user.username
                return redirect(url_for('constrainedmap'))
            else:
                flash(" Incorrect password")
                return redirect(url_for('login'))
        else:
            flash("Username doesn't exist")
            return redirect(url_for('login'))


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return method(*args, **kwargs)
        else:
            flash("A login is required to see the page!")
            return redirect(url_for('constrainedmap'))
    return wrapper


class Main(views.MethodView):
    edges = []
    path = []
    path_bool = [False, False]

    def get(self):
        self.path_bool[0] = True
        return render_template('constrainedmap.html',
                               path_bool=map(dumps, self.path_bool))

    def post(self):
        req = copy(request.form)
        if 'craft' in req:
            user = dict(session)['username']
            query = """SELECT user.id
                       FROM user
                       WHERE user.user = ?;
                    """
            cur = get_db().cursor()
            cur.execute(query, (user,))
            user_id = cur.fetchall()[0][0]
            cur.execute("""INSERT INTO edges(lat_start, lat_end, long_start, long_end, rank, user_id)
                               VALUES (?, ?, ?,?, ?, ?);""", (float(req['start[lat]']),
                                                              float(req['end[lat]']),
                                                              float(req['start[long]']),
                                                              float(req['end[long]']),
                                                              int(req['rank']),
                                                              user_id))
            get_db().commit()
        elif 'walk' in req:
            lat1 = float(req["lat1"])
            lat2 = float(req["lat2"])
            lon1 = float(req["long1"])
            lon2 = float(req["long2"])
            random_walk = [[float(req["lat1"]),
                            float(req["long2"])]]
            get_db().create_function("cos", 1, cos)
            get_db().create_function("sin", 1, sin)
            get_db().create_function("acos", 1, acos)
            get_db().create_function("asin", 1, asin)
            get_db().create_function("distance", 4, distance)
            cur = get_db().cursor()
            print (lat1, lat2, lon1,lon2)

            cur.execute(map_graph.QUERY1, (lat2,
                                           lon2,
                                           lat2,
                                           lon2,
                                           lat1,
                                           lon1,
                                           lat2,
                                           lon2,
                                           lat2,
                                           lon2,
                                           lat1,
                                           lon1,
                                           lat2,
                                           lon2))
            results = cur.fetchall()
            print results
            # breakk
            while len(results) > 0:
                weights = [x[-1] for x in results]
                index = decision_at_node_N(weights)
                random_walk += [[results[index][0],results[index][1]],
                                [results[index][2],results[index][3]]]
                lat1 = float(results[index][0])
                lon1 = float(results[index][1])
                print "1uery params:",(lat1, lat2, lon1,lon2)
                cur.execute(map_graph.QUERY1, (lat2,
                                               lon2,
                                               lat2,
                                               lon2,
                                               lat1,
                                               lon1,
                                               lat2,
                                               lon2,
                                               lat2,
                                               lon2,
                                               lat1,
                                               lon1,
                                               lat2,
                                               lon2))
                results = cur.fetchall()
                print results
            random_walk += [[float(req["lat2"]),
                             float(req["long2"])]]
            print random_walk
            print len(random_walk)

        return redirect(url_for('constrainedmap'))


class LogOut(views.MethodView):

    def get(self):
        session.pop('username', None)
        session['logged_in'] = False
        return redirect(url_for('constrainedmap'))


class SignUp(views.MethodView):
    @ssl_required
    def get(self):
        return render_template('signup.html')

    @ssl_required
    def post(self):
        form = RegistrationForm(request.form)
        username = form.email.data
        address = form.addr.data
        passwd = form.key.data
        passwd2 = form.key2.data
        if passwd2 != passwd:
            flash("Passwords do not match")
            return redirect(url_for('signup'))
        elif not form.validate():
            flash("Required fields missing")
            return redirect(url_for('signup'))
        else:
            user = User(username, passwd, address)
            cur = get_db().cursor()
            print passwd
            print user.pw_hash
            cur.execute("""INSERT INTO user(user, password, postcode)
                           VALUES (?, ?, ?);""", (user.username,
                                                  user.pw_hash,
                                                  user.addr))
            get_db().commit()
            return redirect(url_for('constrainedmap'))


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.create_function("cos", 1, cos)
            db.create_function("sin", 1, sin)
            db.create_function("acos", 1, acos)
            db.create_function("asin", 1, asin)
            db.cursor().executescript(f.read())
            db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

app.add_url_rule('/main',
                 view_func=Main.as_view('constrainedmap'),
                 methods=["GET", "POST"])

app.add_url_rule('/login',
                 view_func=Login.as_view('login'),
                 methods=["GET", "POST"])

app.add_url_rule('/logout',
                 view_func=LogOut.as_view('logout'),
                 methods=["GET", "POST"])

app.add_url_rule('/signup',
                 view_func=SignUp.as_view('signup'),
                 methods=["GET", "POST"])


if __name__ == '__main__':
    # init_db()
    app.run()
