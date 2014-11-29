# imports
import functools
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, views
from contextlib import closing

# confifuration instructions
DATABASE = '/tmp/app.db'
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'
# temporary test database
users = {'test1@gmail.com': '1'}
# login_manager = LoginManager()
# application initiation
app = Flask(__name__)
app.config.from_object(__name__)


class Login(views.MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        if 'logout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))
        # required = ['username', 'password']
        # for r in required:
        #     if r not in request.form:
        #         flash("Error: {0} is required.".format(r))
        #         return redirect(url_for('index'))
        username = request.form['email']
        passwd = request.form['key']
        if username in users and users[username] == passwd:
            session['logged_in'] = True
            session['username'] = username
            print session
            return redirect(url_for('constrainedmap'))
        else:
            flash("Username doesn't exist or incorrect password")
            return redirect(url_for('login'))


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return method(*args, **kwargs)
        else:
            flash("A login is required to see the page!")
            return redirect(url_for('index'))
    return wrapper


class Main(views.MethodView):
    def get(self):
        return render_template('constrainedmap.html')


class LogOut(views.MethodView):

    def get(self):
        session.pop('username', None)
        session['logged_in'] = False
        return redirect(url_for('constrainedmap'))


class SignUp(views.MethodView):

    def get(self):
        return render_template('signup.html')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

app.add_url_rule('/',
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
    app.run()
