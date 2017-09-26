from base import CRUD, db


class Relatorio(db.Model, CRUD):
	__tablename__ = "relatorio"

	id = db.Column(db.Integer, primary_key=True)
	tipo_in_out = db.Column(db.String(1), nullable=False)
	horario = db.Column(db.DateTime, nullable=False)
	acesso_nome_sala = db.Column(db.String(4), db.ForeignKey('acesso.nome_sala'))
	acesso_id_usuario = db.Column(db.Integer, db.ForeignKey('acesso.id_usuario'))

	def __init__(self, tipo_in_out, horario):
		self.tipo_in_out = tipo_in_out
		self.horario = horario
