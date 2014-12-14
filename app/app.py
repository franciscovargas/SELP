# imports
import functools
import sqlite3
import map_graph
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, views, current_app, jsonify
from werkzeug.security import generate_password_hash, \
    check_password_hash
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask.ext.wtf.html5 import EmailField
from contextlib import closing
from copy import copy
from map_graph import  decision_at_node_N, distance
from json import dumps
from math import cos , sin , acos, asin, pi


# configuration instructions
DATABASE = 'app.db'
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'
# application initiation
app = Flask(__name__)
app.config.from_object(__name__)
# global variable used to send path to front end
walk = []

def ssl_required(fn):
    """
    Decorator for https redirection in inscure http
    pages such as login and sigup
    """
    @functools.wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
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
#                                END                                          #
###############################################################################
                              ###########                                     
                              ###########
                              ###########                                     
###############################################################################
#                        VIEW METHOD CLASSES                                  #
###############################################################################
class Login(views.MethodView):
    @ssl_required
    def get(self):
        # small db check
        cur = get_db().cursor()
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
        cur.execute(query, (user.username,))
        result = cur.fetchall()
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
    # The following view attributes provide communication
    # Messages between the client javascrpt mapcon.js and
    # The back end in this  view in order to yield the 
    # dynamic properties held in the view.
    edges = []
    path = []
    path_bool = [False, False]
    ranks_and_keys= []
    user_rank = 0

    def get(self):
        self.path_bool[0] = True
        if 'logged_in' in session and 'username' in session:
            user = dict(session)['username']
            query_rank = """SELECT user.path_count
                            FROM user
                            WHERE user.user = ?;
                         """
            cur = get_db().cursor()
            cur.execute(query_rank, (user,))
            self.user_rank = cur.fetchall()[0][0]
            session['rank'] = self.user_rank
        return render_template('constrainedmap.html',
                               path_bool=map(dumps, self.path_bool))

    def post(self):
        req = copy(request.form)
        rank_path_bool = False

        #Checking for the correct post request
        #To the craft and commit path
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
            query_rank = """SELECT user.path_count
                            FROM user
                            WHERE user.user = ?;
                         """
            cur = get_db().cursor()
            cur.execute(query_rank, (user,))
            self.user_rank = cur.fetchall()[0][0]
            cur.execute(""" UPDATE  user
                            SET path_count=?
                            WHERE user=?;
                        """,(self.user_rank + 1 , user))
            get_db().commit()


        # Checking for the correct post request
        # To compute random biased walk
        elif 'walk' in req:
            lat1 = float(req["lat1"])
            lat2 = float(req["lat2"])
            lon1 = float(req["long1"])
            lon2 = float(req["long2"])
            random_walk = [[float(req["lat1"]),
                            float(req["long2"])]]
            ranks_and_keys  = []
            # Passing methods from python to sql
            get_db().create_function("cos", 1, cos)
            get_db().create_function("sin", 1, sin)
            get_db().create_function("acos", 1, acos)
            get_db().create_function("asin", 1, asin)
            get_db().create_function("distance", 4, distance)
            cur = get_db().cursor()
            # fetches the
            # The following query queries for
            # top 6 paths which take you a step closer to the destination
            # and are within 1Km rangeto the current node you are at
            cur.execute(map_graph.QUERY1, (lat1,
                                           lon1,
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
            # The following loop carries out the query which fetches the
            # top 6 paths which take you a step closer to the destination
            # and are within 1Km rangeto the current node you are at
            # The contraints on the query gaurantee this loop to converge
            # At each iteration it it gets closest to the end point
            # till there are no more points in the database which are closer
            # to the end point. Databases are finite is a key fact here.
            while len(results) > 0:
                weights = [x[-1] for x in results]
                # Dice throwing algorithm to pick on to which node/edge
                # edge to move on to
                index = decision_at_node_N(weights)
                random_walk += [[results[index][0],results[index][1]],
                                [results[index][2],results[index][3]]]
                self.ranks_and_keys += [[results[index][4],results[index][5]]]
                lat1 = float(results[index][0])
                lon1 = float(results[index][1])
                # Distance query execution
                cur.execute(map_graph.QUERY1, (lat1,
                                               lon1,
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
            random_walk += [[float(req["lat2"]),
                             float(req["long2"])]]
            # Global walk variable utilized to pass json to route in
            # order to draw path in the front end
            # whilist this is not good practice or pythonic at all
            # Dealing with theese frameworks is a whole new thing
            # and it was the only way I could figure this out with
            # the given time constraints
            global walk
            walk = copy(random_walk)
            rank_path_bool = True

        # Checking for the correct post
        # Following condition ranks the random path excuted by the client
        # updating all edges contained in that path by
        # averaging the new path with the old one
        elif 'rank_p' in req and len(self.ranks_and_keys) > 0:
            try:
                edge_rank = float(req['rank_p'])
                new_rank = [((float(x[0]) + edge_rank) / 2.0, int(x[1]))
                               for x in self.ranks_and_keys]
                update_query = """ UPDATE  edges
                                   SET rank=?
                                   WHERE id=?;
                               """
                cur = get_db().cursor()
                for edge in new_rank:
                    cur.execute(update_query,(edge[0], edge[1]))
                get_db().commit()
                self.ranks_and_keys = []
            except:
                # flash a inccorrect input message
                pass
                
     
        return redirect(url_for('constrainedmap'))



class LogOut(views.MethodView):
    """
    Simple logging out view method
    """

    def get(self):
        session.pop('username', None)
        session['logged_in'] = False
        return redirect(url_for('constrainedmap'))


class SignUp(views.MethodView):
    """
    Simple signup view method
    """
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
            cur.execute("""INSERT INTO user(user, password, postcode)
                           VALUES (?, ?, ?);""", (user.username,
                                                  user.pw_hash,
                                                  user.addr))
            get_db().commit()
            return redirect(url_for('constrainedmap'))


class About(views.MethodView):
    """
    About view
    """
    def get(self):
        return render_template('about.html')
###############################################################################
#                                END                                          #
###############################################################################
                              ###########                                     
                              ###########
                              ###########                                     
###############################################################################
#                              ROUTES                                         #
###############################################################################

@app.route('/get_walk')
def get_walk():
    """
    This routes utilizes the local variable walk
    in order to host a json which holds the drawing
    coordinates for the computed random walk in the main
    """
    return jsonify(walk=walk, test='test')
###############################################################################
#                                END                                          #
###############################################################################
                              ###########                                     
                              ###########
                              ###########                                     
###############################################################################
#                           DATABASE FUNTIONS                                 #
###############################################################################

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


###############################################################################
#                                END                                          #
###############################################################################
                              ###########                                     
                              ###########
                              ###########                                     
###############################################################################
#                              URL RULES                                      #
###############################################################################


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

app.add_url_rule('/about',
                 view_func=About.as_view('about'),
                 methods=["GET", "POST"])


if __name__ == '__main__':
    app.run()
