from flask import Flask, render_template, session, request, jsonify, Response
from model import entities
from database import connector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

app = Flask(__name__)
db = connector.Manager()

cache = {}
engine = db.createEngine()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    data = request.form

    session = db.getSession(engine)
    users = session.query(entities.User)

    for User in users:
        if User.username == data['username'] and User.password == data['password']:
            return render_template('main.html')

    return "wrong username/password..."

@app.route('/do_signin', methods=['POST'])
def do_signin():
    name = request.form['name']
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    print(name, fullname, username, password)

    user = entities.User(username=username, password=password, name=name, fullname=fullname)

    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return "successful register!!"


@app.route('/foro')
def foro():
    return render_template('main.html', title="foro")

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = "iLikeBananas"
    app.run(port=8080, threaded=True, host='0.0.0.0')