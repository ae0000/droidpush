# -*- coding: utf-8 -*-
"""
    Droidpush
    ~~~~~~

    Pushing it to droid since 2012

    :copyright: (c) 2012 by Andrew Edwards
"""
from __future__ import with_statement
from droidpush import app
from contextlib import closing
from flaskext.mongokit import MongoKit, Document
from datetime import datetime
import re
from models import *
from forms import *
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash

# configuration
MONGODB_DATABASE = 'droidpush'
MONGODB_HOST = 'localhost'
DEBUG = True
SECRET_KEY = 'kçfsdf*عربي*v*&$) رئيسرسّ+==H$&maLk?$عرewبي#1 and there it is'

# create the app
app.config.from_object(__name__)
app.config.from_envvar('DROIDPUSH_SETTINGS', silent=True)

# create the db connection
db = MongoKit(app)
db.register([User])

@app.route('/')
def home():
    return 'ok';
    # cur = g.db.execute('select title, text from entries order by id desc')
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # return render_template('show_entries.html', entries=entries)


@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.User()
        user.email = form.email.data
        user.password = form.password.data
        user.save()
        flash('Your account has been created.')
        return redirect(url_for('dashboard'))

    return render_template('register.html', registeractive=True, form=form)


@app.route('/dashboard')
def dashboard():
    return 'dashboard'

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