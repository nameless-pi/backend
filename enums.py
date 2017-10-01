import enum
from marshmallow import fields


class EnumDia(fields.Field):
	def _serialize(self, value, attr, obj):
		print('VALOOOR ->', value)
		if value is None:
			return ""
		if value == Dia.domingo:
			return "Domingo"
		elif value == Dia.segunda:
			return "Segunda-Feira"
		elif value == Dia.terca:
			return "Terça-Feira"
		elif value == Dia.quarta:
			return "Quarta-Feira"
		elif value == Dia.quinta:
			return "Quinta-Feira"
		elif value == Dia.sexta:
			return "Sexta-Feira"
		elif value == Dia.sabado:
			return "Sábado"


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
			return "Aluno"
		elif value == TipoUsuario.professor:
			return "Professor"
		elif value == TipoUsuario.servente:
			return "Servente"


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
			return "Entrada"
		elif value == Evento.saida:
			return "Saída"


class Evento(enum.Enum):
	entrada = 0
	saida = 1
