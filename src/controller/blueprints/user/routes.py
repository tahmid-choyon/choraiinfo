from flask import Blueprint, request, render_template, redirect, url_for, make_response, jsonify, flash
from flask_login import login_user, current_user, logout_user

from .user_crud import *

user_blueprint = Blueprint("userbp", __name__, static_folder="../../../static", template_folder="../../../templates")


@user_blueprint.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        user, err = create_new_user(username, email, password)
        if err:
            flash(user)
            return redirect(url_for("userbp.user_register"))

        login_user(user)
        return redirect(url_for("userbp.user_login"))


@user_blueprint.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return make_response(jsonify(
                current_user.json
            ), 200)
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not user_check_credential(email, password):
            print("invalid")
            flash("Invalid credentials!")
            return redirect(url_for("userbp.user_login"))

        user = get_user_from_email(email)
        login_user(user)
        print(user.json)
        return make_response(jsonify(
            user.json
        ), 200)


@user_blueprint.route("/logout")
def user_logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("userbp.user_login"))