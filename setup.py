from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
# from flask_cors import CORS


app = Flask(__name__)
api = Api(app)

app.config.from_object("config")

# cors = CORS(app)
db = SQLAlchemy(app)


@app.after_request
def after_request(response):
	response.headers.add("Access-Control-Allow-Origin", "*")
	if request.method == "OPTIONS":
		response.headers.add("Access-Control-Allow-Headers", "*")
		response.headers.add("Access-Control-Allow-Methods", "DELETE, GET, POST, PUT")
		headers = request.headers.get("Access-Control-Request-Headers")
		if headers:
			response.headers.add("Access-Control-Allow-Headers", headers)
	return response

from admin_model import Admin


def authenticate(login, password):
	login = Admin.query.filter(Admin.login == login).first()
	if login and login.verify_password(password):
		return login


def identity(payload):
	user_id = payload["identity"]
	return Admin.query.get(user_id).login


jwt = JWT(app, authenticate, identity)
