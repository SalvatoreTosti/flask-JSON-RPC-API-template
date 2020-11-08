from app import app
from app.interfaces import user
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app.REST import RESTInterface
from app.rpc import JSONRPC


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        return render_template("login.html")

    form = request.form
    return user.login(form["username"], form["password"])


@app.route("/logout")
def logout():
    return user.logout()
