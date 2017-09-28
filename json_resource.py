from marshmallow import Schema, fields
from flask_restful import Resource

from setup import db
from sala_model import Sala


class JSONSchema(Schema):
	nome = fields.String()


schema = JSONSchema()


class JSONResource(Resource):
	def get(self, tipo):
		if tipo == 'salas':
			sala_query = db.session.query(Sala.nome).all()
			result = schema.dump(sala_query, many=True).data
			return result
