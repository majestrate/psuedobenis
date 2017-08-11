from oniichan import app
from oniichan import models
from oniichan import posting
from oniichan import util

from flask import request, jsonify, session

@app.route("/api/post.json", methods=["POST"])
def api_new_post():
    with util.get_session_user_or_abort(403) as user:
        j = request.get_json()
        if 'message' in j:
            posting.newPost(user, j['message'])
            return jsonify({"error": None})
        else:
            return jsonify({"error": "no message"})
