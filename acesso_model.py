from marshmallow import Schema, fields

from base import db, CRUD


class Acesso(db.Model, CRUD):
	__tablename__ = "acesso"

	id = db.Column(db.Integer, primary_key=True)
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
	nome_sala = db.Column(db.String(4), db.ForeignKey('sala.nome'), nullable=False)
	sync = db.Column(db.Boolean, nullable=False)

	def __init__(self, id_usuario, nome_sala):
		self.id_usuario = id_usuario
		self.nome_sala = nome_sala
		self.sync = False


class AcessoSchema(Schema):
	id = fields.Integer()
	nome_sala = fields.String()

	class Meta:
		type_ = 'acesso'
