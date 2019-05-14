from flask import render_template, redirect, url_for, flash, request
from . import auth
from .forms import LoginForm, RegisterationForm, changePasswordForm, resetPasswordForm
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
import logging

log = logging.getLogger("user_operations")
handler = logging.FileHandler("user_operations.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'))
log.addHandler(handler)
log.setLevel(logging.INFO)

@auth.route("/login",  methods=["GET","POST"])
def login():
    loginError = None
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        loginError="Invalid emial or password"
    log.info("Log in operation triggered")
    return render_template("auth/login.html", form=form,loginError=loginError)

@auth.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    log.info("Log out operation triggered")
    flash("You has been logged out.")
    return redirect(url_for("auth.login"))

@auth.route("/register",  methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, username=form.username.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    log.info("register_operation triggered")
    return render_template("auth/register.html", form=form)


@auth.route("/changePassword",  methods=["GET","POST"])
@login_required
def change_password():
    form = changePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        flash("Change password successfully")
        return redirect(url_for("main.index"))
    log.info("change password operation triggered")
    return render_template("auth/changePassword.html", form=form)


@auth.route("/resetPassword/<token>",  methods=["GET","POST"])
def reset_password(token):
    form = resetPasswordForm()
    if form.validate_on_submit():
        user = User.confirm_token_user(token)
        if user:
            user.password = form.password.data
            db.session.add(user)
            login_user(user)
            flash("Reset password Successfully!")
        else:
            flash("Reset password failed!")
            redirect(url_for("auth.main"))
        return redirect(url_for('auth.login'))
    log.info("reset_password operation triggered")
    return render_template("auth/resetPassword.html", form=form)


