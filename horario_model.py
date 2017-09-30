from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from base import CRUD, db
from enums import Dia, TipoUsuario

class Horario(db.Model, CRUD):
	__tablename__ = "horario"

	id = db.Column(db.Integer, primary_key=True)
	last_update = db.Column(db.DateTime, nullable=False)
	dia = db.Column(db.Enum(Dia), nullable=False)
	hora_fim = db.Column(db.Time, nullable=False)
	hora_inicio = db.Column(db.Time, nullable=False)
	tipo_user = db.Column(db.Enum(TipoUsuario), nullable=False)
	id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)

	def __init__(self, id_sala, dia, hora_fim, hora_inicio, tipo_user):
		self.id_sala = id_sala
		self.dia = dia
		self.hora_inicio = hora_inicio
		self.hora_fim = hora_fim
		self.tipo_user = tipo_user
		self.last_update = datetime.now()


class HorarioSchema(Schema):
	id = fields.Integer()
	id_sala = fields.Integer()
	hora_inicio = fields.Time()
	hora_fim = fields.Time()
	dia = EnumField(Dia)
	tipo_user = EnumField(TipoUsuario)
	last_update = fields.DateTime()

	class Meta:
		type_ = 'horario'
