from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_username(self, username):
        if type(username) is not str:
            return
        if len([user for user in User.query.all() if user.username == username]) != 0:
            return
        self.username = username
        db.session.add(self)
        db.session.commit()

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user

    def to_json(self):
        return {"id": self.id, "username": self.username, "email": self.email}

    @staticmethod
    def make_user(username, password):
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return u
