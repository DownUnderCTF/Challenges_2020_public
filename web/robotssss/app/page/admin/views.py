import re
import urllib.parse
from flask import Blueprint, flash, redirect, render_template, render_template_string, request, session, url_for
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, Markup
from flask_login import current_user, logout_user, login_required

from page.models import database, Users
from sqlalchemy import asc, desc
import sqlite3

admin = Blueprint('admin', __name__, url_prefix='/')

html_escape_table = {
    ">": "&gt;",
    "<": "&lt;",
    "_": "",
    "[": "",
    "]": "",
    "5f":"",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

@admin.route('/')
def index():
    return render_template('public.html')

@admin.route('/admin.php', methods=('POST', 'GET'))
@login_required
def profile():
    #print("+++"+str(current_user)+"+++")
    if str(current_user) == "Account name: admin\n":
        ui = ""
        if request.method == 'POST':
            ui = request.form['user_in']
            ui = html_escape(ui)            
            print(ui)
        template = '''{% extends "base.html" %}
            {% block body %}
        
            <style>
                .ins {
                    margin-left: 30px;
                    width: 85%;
                    margin-bottom: 30px;
                }

                .box {
                    margin-left: 30px; 
                }

                .lab {
                    color: black;
                    font-size: 15px;
                    margin-bottom: 10px;
                }

                .inp {
                    width: 38%;
                    margin-bottom: 10px;
                }

                .btn {
                    padding: 7px 18px;
                    margin-bottom: 25px;
                } 

                .echo {
                    font-size: 14px;
                    color: black;
                }
            </style>
        
            </br></br>
            <h4 class="ins">You have reached the admin terminal! I can echo anything you type in.</h4>

            <div class="form-group box">
                <form method="post">
                    <label class="col-form-label lab" for="inputDefault">Enter a string:</label>
                    <input type="text" class="form-control inp" placeholder="e.g hi" name="user_in" id="user_in">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
        '''
        template += '''<p class="echo">You typed: %s</p>
        </div>
        ''' % (ui)
        template += '''{% endblock %}'''
        return render_template_string(template, ui=ui)
    else:
        return  redirect(url_for('user.blogs'))
