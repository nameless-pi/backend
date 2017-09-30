from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_enum import EnumField


from base import CRUD, db
from enums import TipoUsuario
from acesso_model import DireitoAcesso, AcessoSchema


class Usuario(db.Model, CRUD):
	__tablename__ = "usuario"

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(80), nullable=False)
	tipo = db.Column(db.Enum(TipoUsuario), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	rfid = db.Column(db.String(16), nullable=False, unique=True)
	direito_acesso = db.relationship('DireitoAcesso', cascade="delete")
	last_update = db.Column(db.DateTime(), nullable=False)

	def __init__(self, nome, email, rfid, tipo):
		self.nome = nome
		self.email = email
		self.rfid = rfid
		self.tipo = tipo
		self.last_update = datetime.now()


class UsuarioSchema(Schema):
	id = fields.Integer()
	nome = fields.String()
	email = fields.String()
	rfid = fields.String()
	tipo = EnumField(TipoUsuario)
	last_update = fields.DateTime()
	direito_acesso = fields.Nested(AcessoSchema, many=True)

	class Meta:
		type_ = 'usuario'
