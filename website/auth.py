from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db        ##means from __init__.py import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Login successful", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Login failed, bad password, try again", category='error')
        elif email.strip() == "":
            flash("Please enter your email address to Login", category='error')
        else:
            flash("Login failed, this email is not existing", category='error')

        return redirect(url_for('auth.login'))
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email is already registered", category='error')
        elif len(email) < 4:
            flash("Email must be at least 4 characters long", category='error')
        elif len(password1) < 2:
            flash("Password must be at least 2 characters long", category='error')
        elif password1 != password2:
            flash("Passwords do not match", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters long", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash("Sign up successful", category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
