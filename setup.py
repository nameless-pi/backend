from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT


app = Flask(__name__)
api = Api(app, prefix="/api/v1")

app.config.from_object('config')

db = SQLAlchemy(app)

from admin_model import Admin


def authenticate(login, password):
	login = Admin.query.filter(Admin.login == login).first()
	if login and login.verify_password(password):
		return login


def identity(payload):
	user_id = payload['identity']
	return Admin.query.get(user_id).login


jwt = JWT(app, authenticate, identity)
