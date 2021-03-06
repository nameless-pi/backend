from marshmallow import Schema, fields
from passlib.apps import custom_app_context as pwd_context

from base import CRUD, db


class Admin(db.Model, CRUD):
	__tablename__ = "admin"

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(80), nullable=False)
	login = db.Column(db.String(80), nullable=False, unique=True)
	password = db.Column(db.String(128), nullable=False)

	def __init__(self, nome, login, password):
		self.nome = nome
		self.login = login
		self.password = pwd_context.encrypt(password)

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)


class AdminSchema(Schema):
	id = fields.Integer()
	nome = fields.String()
	login = fields.String()

	class Meta:
		type_ = "admin"
