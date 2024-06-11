from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from model import *

auth = Blueprint(
    "auth", __name__,
    template_folder= 'templates',
    static_folder= 'static')

@auth.route("/")
def home():
    return render_template("index.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Check email and password.', category='error')
    return render_template('login.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')

        new_user = User(email=email, username=username, password=hashed_password)


        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            flash('Registration successful!', category='success')
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash('Email address already in use.', category='error')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route("/homepage", methods=['GET', 'POST'])
@login_required
def homepage():
    return render_template("home.html")

@auth.route("/admin")
@login_required
def admin():
    return render_template("admin.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
