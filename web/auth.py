from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST","GET"])
def log_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in succesfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home_page"))
            else:
                flash("Incorect password", category="error")
        else:
            flash("Email does not exist", category="error")
    return render_template("log_in.html", user=current_user)



@auth.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("auth.log_in"))



@auth.route("/signup", methods=["POST","GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password = request.form.get("password")
        con_password = request.form.get("con_password")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash("Email already exists", category="error")
        elif len(email) < 4:
            flash("Email must be at least five characters", category="error")
        elif len(first_name) < 2:
            flash("First Name must be at least three characters", category="error")
        elif password != con_password:
            flash("Passwords do not match", category="error")
        elif len(password) < 6:
            flash("Password must be at least 7 characters", category="error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            
            user = User.query.filter_by(email=email).first()
            
            login_user(user, remember=True)
            flash("Account created", category="success")
            
            return redirect(url_for("views.home_page"))
        
        
    return render_template("sign_up.html", user=current_user)