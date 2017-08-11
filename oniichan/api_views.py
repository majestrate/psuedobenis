from oniichan import app
from oniichan import models

import flask


@app.route("/api/post.json", methods=["POST"])
def api_new_post():
    return flask.jsonify({"error": None})
