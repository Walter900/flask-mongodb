from app import app, lm
from flask import request, redirect, render_template, url_for, flash, jsonify, abort, make_response
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterationForm, EditProfileForm, PostForm, testForm
from .model import User, Temp, Post
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from gridfs import GridFS, NoFile
from app.util import bson_obj_id, AllowFile
from flask import send_from_directory
import bson.binary

UPLOAD_FOLDER = '/Users/Jomin/Desktop/flask-mongdb/app/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/test', methods=['GET', 'POST'])
def upload_file():
    user = app.config['USERS_COLLECTION'].find_one({"username": current_user.username})
    if request.method == 'POST':

        avatar = request.files['file']
        if avatar and allowed_file(avatar.filename):
            fs = GridFS(MongoClient().db, collection="avatar")
            filename = secure_filename(avatar.filename)
            avatar_id = fs.put(avatar, content_type=avatar.content_type, filename=filename)

            if avatar_id:
                    if user['avatar']:
                        fs.delete(user['avatar'])
                    MongoClient().blog.users.update({'email': current_user.email}, {'$set': {'avatar': avatar_id}})
                    flash('successfully upload image')
            else:
                flash('It is not support', 'red')
            
            return redirect(request.args.get("next") or url_for('test2', avatar_id =avatar_id))
    return render_template('test.html')


@app.route('/test2/<avatar_id>', methods=['GET', 'POST'])
def test2(avatar_id):
    avatar_id  =  avatar_id
    u = app.config['USERS_COLLECTION'].find_one({"username": current_user.username})
    avatar = avatar = u['avatar']
    form = testForm()
    if form.validate_on_submit():
        render_template('/uploads/<avatar>')

    return render_template('test2.html', avatar = avatar, avatar_id= avatar_id)




@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
       Post(body=form.body.data).new_article()
       return redirect(request.args.get("next") or url_for("index"))
    return render_template('home.html', form=form)

@app.route('/')
@app.route('/index')
def index():
    posts = MongoClient().blog.aritical.find().sort('issuing_time', DESCENDING)
    return render_template('index.html', posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"email": form.email.data}) 

        if user and User.validate_login(user['password'], form.password.data):
            user_obj = Temp(id = user['_id'],
                            username = user['username'],
                            email = user['email'],
                            password  = user['password'],
                            about_me = user['about_me']
                            )
            login_user(user_obj)



            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("home"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
            
        User(username = form.username.data,
             password = form.password.data,
             email = form.email.data,
             about_me = form.about_me.data
            ).new_user()

        flash("Register successfully!", category='success')
        return redirect(request.args.get("next") or url_for("index"))
    return render_template('register.html', form=form)       

@app.route('/profile')
@login_required
def user():
    u = app.config['USERS_COLLECTION'].find_one({"username": current_user.username})
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for(''))
    username = u['username']
    email = u['email']
    about_me = u['about_me']
    avatar = u['avatar']

    #fs = GridFS(MongoClient().db, "avatar")
    #img = fs.get(avatar)
    #data = img.read()

    return render_template('profile.html', username=username, email=email, about_me=about_me,
        avatar = avatar) 


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        MongoClient().blog.users.update({'email': current_user.email}, {'$set': {'username': form.username.data}})
        MongoClient().blog.users.update({'email': current_user.email}, {'$set': {'about_me': form.about_me.data}})
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        name = current_user.username
        flash('Information Changed')
        return redirect(request.args.get("next") or url_for('/profile'))
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@app.route('/uploads/<avatar>')
def uploaded_file(avatar):
    avatarid = avatar
    if avatarid is None:
        return ''
    try:    
      fs = GridFS(MongoClient().db, 'avatar')
      img = fs.get(bson_obj_id(avatarid))
      #data = img.read()
      response = make_response(img.read())
      response.headers['Content-Type'] = img.content_type
      return response
    except NoFile:
      abort(404)

@app.route('/static/avatar/<oid>')
def avatar(oid):
    oid = avatar
    if oid is None:
        return ''
    try:
        fs = GridFS(MongoClient().dbs, "avatar")
        img = fs.get(oid)
        response = make_response(img.read())
        response.headers['Content-Type'] = img.content_type
        return response
    except NoFile:
        abort(404)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    return render_template('write.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"username": username})
    if not u:
        return None
    return Temp(u['_id'],u['username'],u['email'],u['password'],u['about_me'])
