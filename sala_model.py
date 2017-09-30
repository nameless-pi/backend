from marshmallow import Schema, fields

from base import CRUD, db
from horario_model import HorarioSchema


class Sala(db.Model, CRUD):
	__tablename__ = "sala"

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(4), unique=True)
	horarios = db.relationship('Horario', cascade="delete")
	acesso = db.relationship('DireitoAcesso', cascade="delete")

	def __init__(self, nome):
		self.nome = nome


class SalaSchema(Schema):
	id = fields.Integer()
	nome = fields.String()
	horarios = fields.Nested(HorarioSchema, many=True)

	class Meta:
		type_ = 'sala'
