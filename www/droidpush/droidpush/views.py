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
from mongokit import *
from flaskext.gravatar import Gravatar
from flaskext.login import LoginManager, login_user, login_required, logout_user
from datetime import datetime
import re
import logging
from models import *
from forms import *
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash

# configuration
MONGODB_DATABASE = 'droidpush'
MONGODB_HOST = '127.0.0.1'
DEBUG = True
SECRET_KEY = 'kçfsdf*عربي*v*&$) رئيسرسّ+==H$&maLk?$عرewبي#1 and there it is'

# create the app
app.config.from_object(__name__)
app.config.from_envvar('DROIDPUSH_SETTINGS', silent=True)

# setup logging
#logging.basicConfig(filename='droidpush.log',level=logging.DEBUG)

# setup loginmanager
login_manager = LoginManager()
login_manager.setup_app(app)

# create the db connection
db = Connection()
db.register([User])

# setup gravatar
gravatar = Gravatar(app,
    size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False)

@login_manager.user_loader
def load_user(userid):
    # load the user from the model
    user = User()
    if user.load_user(userid):
        return user
    else:
        return None

@app.route('/')
def home():
    return render_template('home.html', homeactive=True)

@app.route('/about')
def about():
    return render_template('about.html', aboutactive=True)

@app.route('/contact')
def contact():
    return render_template('contact.html', aboutactive=True)

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.User()
        user.email = form.email.data
        salt_and_hash = hash_password(form.password.data)
        user.salt = salt_and_hash[0]
        user.password = salt_and_hash[1]
        user.save()

        # now, log the user in
        if user.validate_login(form.email.data,form.password.data):
            # login credentials all good, set the user (which has now been
            # populated with the user details)
            login_user(user)
            flash('Your account has been created.')
            return redirect(url_for('dashboard'))

    return render_template('register.html', registeractive=True, form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Login user, check for remember me
        remember_me =  form.remember.data == 'y'
        user = form.get_user()
        login_user(user, remember=remember_me)
        return redirect(url_for('dashboard'))

    return render_template('login.html', loginactive=True, form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', dashboardactive=True)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))