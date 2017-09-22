from marshmallow import Schema, fields

from base import CRUD, db
from acesso_model import Acesso, AcessoSchema


class Usuario(db.Model, CRUD):
	__tablename__ = "usuario"

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	rfid = db.Column(db.String(16), nullable=False, unique=True)
	acessos = db.relationship('Acesso', cascade="delete")

	def __init__(self, nome, email, rfid):
		self.nome = nome
		self.email = email
		self.rfid = rfid


class UsuarioSchema(Schema):
	id = fields.Integer()
	nome = fields.String()
	email = fields.String()
	rfid = fields.String()
	acessos = fields.Nested(AcessoSchema, many=True)

	class Meta:
		type_ = 'usuario'
