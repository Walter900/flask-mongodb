from flask import Flask
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap=Bootstrap(app)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views
