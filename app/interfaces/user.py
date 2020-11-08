from app import db
from app.models.user import User
from flask import redirect, flash, url_for
from flask_login import current_user, login_user, logout_user


def login(username, password, invalid_redirect="login", authenticated_redirect="index"):
    if current_user.is_authenticated:
        return redirect(url_for(authenticated_redirect))
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        flash("invalid username or password")
        return redirect(url_for(invalid_redirect))
    login_user(user, password)
    return redirect(url_for(authenticated_redirect))


def logout(default_redirect="index"):
    logout_user()
    return redirect(url_for(default_redirect))


def createUser(username, email, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        u = User(username=username, email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()


def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    db.session.delete(user)
    db.session.commit()
