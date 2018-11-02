from flask import Flask, render_template, session, request, jsonify, Response, Blueprint
from model import entities
from database import connector
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


@app.route('/users/<id>', methods = ['PUT'])
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
    c = request.get_json(silent=True)
    db_session = db.getSession(engine)
    user_from = db_session.query(entities.User
                                 ).filter(entities.User.id == c['user_from_id']).first()

    post = entities.Post(content=c['content'],
                               user_from=user_from,
                               sent_on=datetime.datetime.utcnow()
                               )
    db_session.add(post)
    db_session.commit()
    return "Your post has been uploaded"


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
        post.user_from_id = request.form['password']
        post.user_from = request.form['user_from']
        db_session.add(post)
    db_session.commit()
    return "Message updated"


@app.route('/messages/<id>', methods = ['DELETE'])
def delete_message(id):
    db_session = db.getSession(engine)
    posts = db_session.query(entities.Post).filter(entities.Post.id == id)
    for post in posts:
        db_session.delete(post)
    db_session.commit()
    return "Message deleted"


if __name__ == '__main__':
    app.secret_key = "iLikeBananas"
    app.run(port=8080, threaded=True, host='0.0.0.0')
