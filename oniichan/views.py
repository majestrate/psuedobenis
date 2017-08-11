from oniichan import app
from oniichan import db
from oniichan import templates
from oniichan import config
from oniichan import spam
from oniichan import util
from oniichan.lib import audio
import flask
from flask import render_template as template
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps
import io
import os
import string



@app.route("/login", methods=["GET", "POST"])
def oniichan_login():
    """
    user login route
    """
    if flask.request.method == 'POST':
        form = flask.request.form
        with db.open() as session:
            if session.check_local_login(form["username"], form["password"]):
                return redirect(url_for("/user/{}".format(form["username"])))
            else:
                flash("login failed")
    return template("login.html", title="log in")

@app.route("/")
def oniichan_index():
    """
    serve index page
    """
    return template("index.html", title="oniichan engine")
