import enum
from marshmallow import fields


class EnumDia(fields.Field):
	def _serialize(self, value, attr, obj):
		if value is None:
			return ""
		if value == Dia.Domingo:
			return "Domingo"
		elif value == Dia.Segunda:
			return "Segunda"
		elif value == Dia.Terca:
			return "Terca"
		elif value == Dia.Quarta:
			return "Quarta"
		elif value == Dia.Quinta:
			return "Quinta"
		elif value == Dia.Sexta:
			return "Sexta"
		elif value == Dia.Sabado:
			return "Sabado"


class Dia(enum.Enum):
	Domingo = 1
	Segunda = 2
	Terca = 3
	Quarta = 4
	Quinta = 5
	Sexta = 6
	Sabado = 7


class EnumTipo(fields.Field):
	def _serialize(self, value, attr, obj):
		if value is None:
			return ""
		if value == TipoUsuario.Aluno:
			return "Aluno"
		elif value == TipoUsuario.Professor:
			return "Professor"
		elif value == TipoUsuario.Servente:
			return "Servente"


class TipoUsuario(enum.Enum):
	Aluno = 1
	Professor = 2
	Servente = 3


class EnumEvento(fields.Field):
	def _serialize(self, value, attr, obj):
		if value is None:
			return ""
		if value == Evento.entrada:
			return "entrada"
		elif value == Evento.saida:
			return "saida"


class Evento(enum.Enum):
	entrada = 0
	saida = 1
