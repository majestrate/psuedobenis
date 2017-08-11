from oniichan import app
from oniichan import models
from oniichan import templates
from oniichan import config
from oniichan import util
import flask
from flask import render_template as template
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps
import io
import os
import string



@app.route("/login/", methods=["GET", "POST"])
def oniichan_login():
    """
    user login route
    """
    if flask.request.method == 'POST':
        form = flask.request.form
        username = form['username']
        if models.check_local_login(username, form["password"]):
            return redirect(url_for("/u/{}".format(username)))
        else:
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
        return redirect(url_for(oniichan_register_serve))
    u = models.create_local_user(username, form['password'])
    return redirect(u.url())


@app.route("/")
def oniichan_index():
    """
    serve index page
    """
    return template("index.html", title="oniichan engine")
