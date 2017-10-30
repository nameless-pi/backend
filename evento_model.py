from base import CRUD, db
from enums import Evento, EnumEvento
from datetime import datetime
from marshmallow import Schema, fields


class Evento(db.Model, CRUD):
	__tablename__ = "eventos"

	id = db.Column(db.Integer, primary_key=True)
	evento = db.Column(db.Enum(Evento), nullable=False)
	horario = db.Column(db.DateTime, nullable=False)
	# id_direito_acesso = db.Column(db.Integer, db.ForeignKey("direito_acesso.id"))
	id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
	id_sala = db.Column(db.Integer, db.ForeignKey("sala.id"), nullable=False)

	def __init__(self, evento, horario, id_usuario, id_sala):
		self.evento = evento
		self.horario = horario
		self.id_usuario = id_usuario
		self.id_sala = id_sala

class EventoSchema(Schema):
	id = fields.Integer()
	evento = EnumEvento()
	horario = fields.DateTime()
	id_usuario = fields.Integer()
	id_sala = fields.Integer()