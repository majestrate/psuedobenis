from oniichan import db
from oniichan import util

class LocalUser(db.Model):
    """
    Locally owned user
    """

    __tablename__ = "localusers"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    logincred = db.Column(db.String)
    loginsalt = db.Column(db.String)

    def __init__(self, username, password):
        """
        """
        salt = util.new_salt()
        self.logincred = util.hash_func(password, salt)
        self.loginsalt = salt
        self.username = username

    def check_login(self, password):
        """
        check login for correctness
        """
        return util.hash_func(password, self.loginsalt) == self.logincred


def get_user_by_name(username):
    return LocalUser.query.filter_by(username = username).first()


def check_local_login(username, password):
    """
    checks local user login credential
    returns true if it is a valid login
    otherwise returns false
    """
    user = get_user_by_name(username)
    if user is None:
        return False
    return user.check_login(password)