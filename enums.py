import enum
from marshmallow import fields


class EnumDia(fields.Field):
	def _serialize(self, value, attr, obj):
		if value is None:
			return ""
		if value == Dia.domingo:
			return "domingo"
		elif value == Dia.segunda:
			return "segunda"
		elif value == Dia.terca:
			return "terca"
		elif value == Dia.quarta:
			return "quarta"
		elif value == Dia.quinta:
			return "quinta"
		elif value == Dia.sexta:
			return "sexta"
		elif value == Dia.sabado:
			return "sabado"


class Dia(enum.Enum):
	domingo = 1
	segunda = 2
	terca = 3
	quarta = 4
	quinta = 5
	sexta = 6
	sabado = 7


class EnumTipo(fields.Field):
	def _serialize(self, value, attr, obj):
		print('VALOOOR ->', value)
		if value is None:
			return ""
		if value == TipoUsuario.aluno:
			return "aluno"
		elif value == TipoUsuario.professor:
			return "professor"
		elif value == TipoUsuario.servente:
			return "servente"


class TipoUsuario(enum.Enum):
	aluno = 1
	professor = 2
	servente = 3


class EnumEvento(fields.Field):
	def _serialize(self, value, attr, obj):
		print('VALOOOR ->', value)
		if value is None:
			return ""
		if value == Evento.entrada:
			return "entrada"
		elif value == Evento.saida:
			return "saida"


class Evento(enum.Enum):
	entrada = 0
	saida = 1
