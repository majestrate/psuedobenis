from oniichan import app
from oniichan import models
from oniichan import templates
from oniichan import config
from oniichan import util
import flask
from flask import render_template as template
from flask import session
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps
import io
import os
import string
import logging

from contextlib import contextmanager

log = logging.getLogger(__name__)

@contextmanager
def get_session_user_or_abort(code):
    if 'user' in session:
        u = session["user"]
        yield models.get_user_by_name(u)
    else:
        flask.abort(code)

def is_logged_in():
    return 'user' in session

@app.route("/login/", methods=["GET", "POST"])
def oniichan_login():
    """
    user login route
    """
    if flask.request.method == 'POST':
        form = flask.request.form
        username = form['username']
        u = models.check_local_login(username, form["password"])
        if u:
            session["user"] = u.username
            return redirect("/u/{}/".format(username))
        else:
            log.warn("login failed for {}".format(username))
            flash("login failed")
    return template("login.html", title="log in")


@app.route("/register/", methods=["GET"])
def oniichan_register_serve():
    return template("register.html", title="register new account")

@app.route("/register/", methods=["POST"])
def oniichan_register_handler():
    """
    handle register event
    """
    form = flask.request.form
    username = form['username']
    if models.has_user(username):
        flash("username taken")
        return redirect("/register/")
    models.create_local_user(username, form['password'])
    return redirect("/login/")


@app.route("/")
def oniichan_index():
    """
    serve index page
    """
    if is_logged_in():
        with get_session_user_or_abort(404) as user:
            return redirect(user.url())
    return template("index.html", title="oniichan engine")

@app.route("/logout/")
def oniichan_logout():
    if is_logged_in():
        del session["user"]
    return redirect("/")
