import enum


class Dia(enum.Enum):
	domingo = 1
	segunda = 2
	terca = 3
	quarta = 4
	quinta = 5
	sexta = 6
	sabado = 7


class TipoUsuario(enum.Enum):
	aluno = 1
	professor = 2
	servente = 3


class Evento(enum.Enum):
	entrada = 0
	saida = 1
