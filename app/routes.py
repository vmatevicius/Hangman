from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required
from app import db, app, bcrypt
from app.models.account_model import Account
import forms.forms as forms


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")


@app.route("/landing_page", methods=["GET"])
def landing_page():
    return render_template("landing_page.html")


@app.route("/login", methods=["GET", "POST"])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("index"))
            else:
                flash("Login failed, wrong password ", "danger")
        else:
            flash("Login failed, user does not exist", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("landing_page"))


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = forms.RegistrationForm()
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)
