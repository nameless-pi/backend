from base import CRUD, db
from enums import Evento


class Eventos(db.Model, CRUD):
	__tablename__ = "eventos"

	id = db.Column(db.Integer, primary_key=True)
	evento = db.Column(db.Enum(Evento), nullable=False)
	horario = db.Column(db.DateTime, nullable=False)
	id_direito_acesso = db.Column(db.Integer, db.ForeignKey('direito_acesso.id'))

	def __init__(self, evento, horario):
		self.evento = evento
		self.horario = horario
