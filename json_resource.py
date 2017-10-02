from flask_jwt import jwt_required
from flask_restful import Resource
from marshmallow import Schema, fields

from setup import db
from sala_model import Sala


class JSONSchema(Schema):
	id = fields.Integer()
	nome = fields.String()


schema = JSONSchema()


class JSONResource(Resource):
	@jwt_required()
	def get(self, tipo):
		if tipo == "salas":
			sala_query = db.session.query(Sala.id, Sala.nome).all()
			result = schema.dump(sala_query, many=True).data
			return result
