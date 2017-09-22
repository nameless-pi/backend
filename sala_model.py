from marshmallow import Schema, fields

from base import CRUD, db
from acesso_model import Acesso
from horario_model import Horario, HorarioSchema


class Sala(db.Model, CRUD):
	__tablename__ = "sala"

	nome = db.Column(db.String(4), primary_key=True)
	horarios = db.relationship('Horario', cascade="delete")
	acesso = db.relationship('Acesso', cascade="delete")

	def __init__(self, nome):
		self.nome = nome


class SalaSchema(Schema):
	nome = fields.String()
	horarios = fields.Nested(HorarioSchema, many=True)

	class Meta:
		type_ = 'sala'
