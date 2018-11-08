from flask import Flask, render_template, session, request, jsonify, Response, Blueprint,flash
from bs4 import BeautifulSoup
from model import entities
from database import connector
from tkinter import *
import tkinter.messagebox
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import datetime

app = Flask(__name__)
db = connector.Manager()

cache = {}
engine = db.createEngine()

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'),404

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('500.html'),500

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/do_login', methods=['POST'])
def do_login():
    data = request.form

    sessiondb = db.getSession(engine)
    users = sessiondb.query(entities.User)

    for User in users:
        if User.username == data['username'] and User.password == data['password']:
            session['logged'] = True
            return render_template('main.html')
        else:
            flash('fail to login')
            return render_template('index.html')


@app.route('/current_user', methods = ['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.id == session['logged_user_id']
    ).first()
    return Response(json.dumps(user,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')

@app.route('/do_signin', methods=['POST'])
def do_signin():
    name = request.form['name']
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    #print(name, fullname, username, password)

    user = entities.User(username=username, password=password, name=name, fullname=fullname)

    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return "successful register!!"


@app.route('/foro')
def foro():
        if session.get('logged') == True:
            return \
                render_template('main.html')
        else:
            flash('You are not logged in!')
            return render_template('index.html')


@app.route('/latest_posts')
def get_posts():
    return render_template('main.html')

@app.route('/announcements')
def announcements():
    return render_template('announcements.html')


@app.route('/calendar')
def calendar():
        if session.get('logged') == True:
            return \
                render_template('calendar.html')
        else:
            flash('You are not logged in!')
            return render_template('index.html')

  
@app.route('/logout')
def logout():
    session.clear()
    session.pop('logged', None)
    return render_template('index.html')


@app.route('/users', methods =['GET'])
def users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    data = []
    for user in users:
        data.append(user)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    data = []
    for user in users:
        data.append(user)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')


@app.route('/users', methods = ['PUT'])
def update_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        user.name = request.form['name']
        user.fullname = request.form['fullname']
        user.password = request.form['password']
        user.username = request.form['username']
        db_session.add(user)
    db_session.commit()
    return "User updated"


@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        db_session.delete(user)
    db_session.commit()
    return "User deleted"

app.register_blueprint(errors)


@app.route('/do_post')
def do_post():
    return render_template('post.html')


@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.form['title']
    content = request.form['content']
    user_from = request.form['user_from']
    post = entities.Post(title=title, content=content, posted_on=datetime.datetime.utcnow(), user_from=user_from)
    session = db.getSession(engine)
    session.add(post)
    session.commit()

    return render_template('main.html')


@app.route('/posts', methods = ['GET'])
def posts():
    db_session = db.getSession(engine)
    posts = db_session.query(entities.Post)
    data = []
    for post in posts:
        data.append(post)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')


@app.route('/posts/<id>', methods = ['GET'])
def get_post(id):
    db_session = db.getSession(engine)
    posts = db_session.query(entities.Post).filter(entities.Post.id == id)
    data = []
    for post in posts:
        data.append(post)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')


@app.route('/posts/<id>', methods = ['PUT'])
def update_posts(id):
    db_session = db.getSession(engine)
    posts = db_session.query(entities.Post).filter(entities.Post.id == id)
    for post in posts:
        post.content = request.form['content']
        post.sent_on = request.form['sent_on']
        post.user_from_id = request.form['user_from_id']
        post.user_from = request.form['user_from']
        db_session.add(post)
    db_session.commit()
    return "Message updated"


@app.route('/posts/<id>', methods = ['DELETE'])
def delete_message(id):
    db_session = db.getSession(engine)
    posts = db_session.query(entities.Post).filter(entities.Post.id == id)
    for post in posts:
        db_session.delete(post)
    db_session.commit()
    return "Post deleted"

@app.route('/crud_posts', methods=['GET'])
def crud_posts():
    return render_template("crud_posts.html")

@app.route('/clean_posts', methods = ['GET'])
def clean_posts():
    db_session = db.getSession(engine)
    posts = db_session.query(entities.Post)
    for post in posts:
        db_session.delete(post)

    db_session.commit()
    return "Todos los posts eliminados"


@app.route('/crud_users', methods=['GET'])
def crud_users():
    return render_template("crud_users.html")


if __name__ == '__main__':
    app.secret_key = "iLikeBananas"
    app.run(port=8080, threaded=True, debug=True, host='0.0.0.0')
