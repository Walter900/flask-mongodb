from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterationForm, EditProfileForm
from .model import User, Temp
from pymongo import MongoClient

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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
                            about_me = user['about_me'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("write"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        User(username = form.username.data,
             password = form.password.data,
             email = form.email.data,
             about_me=form.about_me.data
            ).new_user()
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
    return render_template('profile.html', username=username, email=email, about_me=about_me) 


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
    return User(u['username'],u['email'],u['password'],u['about_me'])
