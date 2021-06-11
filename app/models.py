from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    This is the class which we will use to create the users for the app
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    bio = db.Column(db.String)
    profile_pic = db.Column(db.String)
    pitches = db.relationship("Pitch", backref="user", lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    pass_locked = db.Column(db.String)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError("You cant always get it right")

    @password.setter
    def password(self, password):
        self.pass_locked = generate_password_hash(password)

    def verify_pass(self, password):
        return check_password_hash(self.pass_locked, password)

    def get_user_pitches(self):
        user = User.query.filter_by(id=self.id).first()
        return user.pitches

    def get_user_comments(self):
        user = User.query.filter_by(id=self.id).first()
        return user.comments


