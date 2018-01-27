# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = "ABC"
USERNAME = $USER
PASSWORD = $PASSWORD

# create out little application :)
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()
    print(g)
    print(g.db)


@app.teardown_request
def teardown_request(exception):
    print("teardown")
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title,text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    print(entries)
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['GET'])
def add_entry():
    print(request.args['title'])
    # if not session.get('logged_in'):
    # abort(401)
    g.db.execute('insert into entries(title,text) values(?,?)',
                 [request.args['title'], request.args['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run("0.0.0.0")
