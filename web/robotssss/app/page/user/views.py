import sqlite3
from flask import current_app
from flask import send_from_directory
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user, login_required
from page import database
from page.models import database, Users, Blog
from page.util.security import generate_confirmation_token, confirm_token
from sqlalchemy import asc
from datetime import datetime
import os

user = Blueprint('user', __name__, url_prefix='/')

'''
Landing page
'''
@user.route('/')
def index():
    return render_template('public.html')

@user.route('/Bender')
def b():
    return render_template('Bender.html')

'''
Logout function
'''
@user.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('user.index'))

@user.route('/humen.txt')
def humen():
    return render_template('humen.txt')

@user.route('/humans.txt')
def humanstxt():
    return render_template('humans.txt')

@user.route('/4dm1n_Cr3ds')
def fakecreds():
    return render_template('fakecreds.html')

'''
Signup function
'''
@user.route('/signUp', methods=('POST', 'GET'))
def signUp():
    # checks to ensure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    # get the POST data from the form
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        confirmed_email = request.form['cEmail']
        password = request.form['password']
        confirmed_password = request.form['cPassword']

        # now we need to check if sign up info is valid
        err = ''
        if not username or not email or not password:
            err += '\n Missing information'
        userExist = Users.query.filter_by(username=username).first()
        if userExist is not None:
            err += '\n Username is taken'
        userExist = Users.query.filter_by(email=email).first()
        if userExist is not None:
            err += '\n Email has been registered already'
        # check to make sure both email supplied are the same
        if email != confirmed_email:
            err += '\n Email provided are not the identical'
        # check to make sure both password supplied are the same
        if password != confirmed_password:
            err += '\n Password provided are not the identical'

        # show error message
        if err == '':
            # create a session to authenticate user
            newUser = Users(username, email, password, "user")
            database.session.add(newUser)
            database.session.commit()
            login_user(newUser)
            return redirect(url_for('user.blogs'))

        flash(err)
    return render_template('signUp.html')

@user.route('/login', methods=('POST', 'GET'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    err = ''
    # get the post request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "" or password == "":
            err += '\n Username or password is wrong'
        elif str(username) == "admin":
            adminExist = Users.query.filter_by(username=str(username)).filter_by(password=str(password)).first()
            if adminExist is None:
                err += '\n Username or password is wrong'
            else:
                adminCheck = Users.query.filter_by(username=str(username)).first()
                print(adminCheck)
                login_user(adminCheck)
                return redirect(url_for('admin.profile'))
        else:
            userExist = Users.query.filter_by(username=str(username)).filter_by(password=str(password)).first()
            if userExist is None:
                err += '\n Username or password is wrong'
            else:
                user = Users.query.filter_by(username=str(username)).first()
                login_user(user)
                return redirect(url_for('user.blogs'))

        flash(err)

    return render_template("login.html")

@user.route('/robot_blogs')
@login_required
def blogs():
    return render_template("blogs.html")

@user.route('/robot_blogs/1')
@login_required
def human():
    return render_template("humans.html") 


@user.route('/robot_blogs/2')
@login_required
def flag_path():
    return render_template("flagp.html")
