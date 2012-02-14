# -*- coding: utf-8 -*-
"""
    Droidpush
    ~~~~~~

    Pushing it to droid since 2012

    :copyright: (c) 2012 by Andrew Edwards
"""
from __future__ import with_statement
from droidpush import app
from droidpush.models import User
from sqlite3 import dbapi2 as sqlite3
#from contextlib import closingl
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mongokit import MongoKit, Document


# configuration
MONGODB_DATABASE = 'droidpush'
MONGODB_HOST = 'localhost'
DEBUG = True
SECRET_KEY = 'kçfsdf*عربي*v*&$) رئيسرسّ+==H$&maLk?$عرewبي#1 and there it is'

# create our little application :)
app.config.from_object(__name__)
app.config.from_envvar('DROIDPUSH_SETTINGS', silent=True)

db = MongoKit(app)
db.regiser([User])

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    #g.db = MongoKit(app)


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    #if hasattr(g, 'db'):
    #    g.db.close()

@app.route('/register', methods=['POST','GET'])
def register():
    return render_template('register_user.html')

@app.route('/')
def home():
    db.User.find()
    return 'hi'

# @app.route('/')
# def show_entries():
#     cur = g.db.execute('select title, text from entries order by id desc')
#     entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
#     return render_template('show_entries.html', entries=entries)



# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     g.db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     g.db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)


# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
