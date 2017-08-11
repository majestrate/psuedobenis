from oniichan import app
from oniichan import models
from oniichan import templates

import flask
from flask import render_template as template
from flask import flash, redirect, url_for



@app.route("/u/<username>/", methods=["POST"])
def ostatus_inbox(username):
    with models.visit_user_or_error(username, 404) as user:
        return ""
