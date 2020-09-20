from flask import Flask, request, redirect, jsonify, render_template, flash, url_for
import pymysql
import os
import time

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'circlespace')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'circlespace')
DB_DATABASE = os.getenv('DB_DATABASE', 'circlespace')

app = Flask(__name__)
app.secret_key = 'mY8afBe1jxJyyfvjJ-_jj2a2PHpsHlj6a5mkGQv2zJN8mSVRUSnWS18QDFBNQTGxxlaldo6kL5cIPnIHzmjtwA'


db = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    charset='utf8mb4',
    autocommit=True,
    database=DB_DATABASE,
    cursorclass=pymysql.cursors.DictCursor)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/create', methods=['POST'])
def create_circle():
    name = request.form.get('name')
    if not name:
        return render_template('error.html', error="Invalid name"), 400
    
    # just truncate to 12
    name = name[:12]
    
    # db connection timeout fix
    db.ping(reconnect=True)
    with db.cursor() as cursor:
        sql = 'INSERT INTO circle (name) VALUES (%s) RETURNING permalink'
        cursor.execute(sql, (name, ))
        res = cursor.fetchone()
        return redirect(url_for('get_circle', permalink=res["permalink"], _external=True,   _scheme="https"))

@app.route('/circle/<permalink>', methods=['GET'])
def get_circle(permalink):
    # db connection timeout fix
    db.ping(reconnect=True)
    
    with db.cursor() as cursor:
        # check if circle exists and get id
        sql_circle = 'SELECT id, name FROM circle WHERE permalink=%s'
        cursor.execute(sql_circle, (permalink, ))
        result = cursor.fetchone()
        if not result:
            return render_template('error.html', error="Circle not found"), 404
        _id = result["id"]
        name = result["name"]
        
        sql_num = 'SELECT COUNT(*) as count FROM people WHERE circle_id=%s'
        cursor.execute(sql_num, (_id, ))
        result = cursor.fetchone()
        count = result['count']

        if count == 0:
            return render_template('circle.html', name=name, info="circle is empty")
        
        sql_rand_person = 'SELECT name FROM people WHERE circle_id=%s ORDER BY RAND() LIMIT 1'
        cursor.execute(sql_rand_person, (_id, ))
        result = cursor.fetchone()
        return render_template(
            'circle.html',
            name=name,
            info=f'{result["name"]} and {count - 1} others are part of your circle'
        )


@app.route('/circle/<permalink>/people', methods=['POST'])
def add_circle_person(permalink):
    name = request.form.get('name')
    if not name:
        return render_template('error.html', error="Invalid name"), 400

    # just truncate to 12
    name = name[:12]
    
    # db connection timeout fix
    db.ping(reconnect=True)
    
    with db.cursor() as cursor:
        # check if circle exists and get id
        sql_circle = 'SELECT id, name FROM circle WHERE permalink=%s'
        cursor.execute(sql_circle, (permalink, ))
        result = cursor.fetchone()
        if not result:
            return render_template('error.html', error="Circle not found"), 404
        _id = result["id"]
        
        sql_insert = f'INSERT INTO people (name, circle_id) VALUES (%s, %s)'
        cursor.execute(sql_insert, (name, _id))
        return redirect(url_for('get_circle', permalink=permalink, _external=True,   _scheme="https"))

@app.route('/circle/<permalink>/people', methods=['GET'])
def get_circle_person(permalink):
    name = request.args.get('name')
    if not name:
        return render_template('error.html', error="Invalid name"), 400

    # db connection timeout fix
    db.ping(reconnect=True)

    with db.cursor() as cursor:
        # check if circle exists and get id
        sql_circle = 'SELECT id, name FROM circle WHERE permalink=%s'
        cursor.execute(sql_circle, (permalink, ))
        result = cursor.fetchone()
        if not result:
            return render_template('error.html', error="Circle not found"), 404
        _id = result["id"]

        if "sleep" in name.lower():
            flash(f'{name} is not part of your circle')
            return redirect(url_for('get_circle', permalink=permalink, _external=True,   _scheme="https"))
        
        # this is where it's broken
        # i dont think a normal app would look lk this as it's only broken in this place
        try:
            sql_exists= f'SELECT name FROM people WHERE circle_id={_id} AND name="{name}"'
            cursor.execute(sql_exists)
            result = cursor.fetchone()
            
            if result:
                flash(f'{name} is part of your circle')
            else:
                flash(f'{name} is not part of your circle')
            return redirect(url_for('get_circle', permalink=permalink, _external=True,   _scheme="https"))
        except:
            flash(f'{name} is not part of your circle')
            return redirect(url_for('get_circle', permalink=permalink, _external=True,   _scheme="https"))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', error="Page not found"), 404
