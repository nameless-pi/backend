from marshmallow import Schema, fields

from base import CRUD, db


class Horario(db.Model, CRUD):
	__tablename__ = "horario"

	id = db.Column(db.Integer, primary_key=True)
	sync = db.Column(db.Boolean, nullable=False)
	dia = db.Column(db.String(15), nullable=False)
	hora_fim = db.Column(db.DateTime, nullable=False)
	hora_inicio = db.Column(db.DateTime, nullable=False)
	tipo_user = db.Column(db.String(10), nullable=False)
	nome_sala = db.Column(db.String(4), db.ForeignKey('sala.nome'), nullable=False)

	def __init__(self, nome_sala, hora_fim, hora_inicio, dia, tipo_user, sync):
		self.nome_sala = nome_sala
		self.hora_fim = hora_fim
		self.hora_inicio = hora_inicio
		self.dia = dia
		self.tipo_user = tipo_user
		self.sync = sync


class HorarioSchema(Schema):
	id = fields.Integer()
	nome_sala = fields.String()
	hora_inicio = fields.DateTime()
	hora_fim = fields.DateTime()
	dia = fields.String()
	tipo_user = fields.String()
	sync = fields.Boolean()

	class Meta:
		type_ = 'horario'
