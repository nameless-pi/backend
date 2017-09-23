from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from admin_model import Admin, AdminSchema

schema = AdminSchema()


class AdminResource(Resource):
	@jwt_required()
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("login", type=str, required=True, location='json')
		parser.add_argument("senha", type=str, required=True, location='json')

		args = parser.parse_args(strict=True)

		try:
			admin = Admin(args["login"], args["senha"])
			admin.add(admin)
			query = Admin.query.get(admin.login)
		except SQLAlchemyError as e:
			db.session.rollback()
			response = jsonify({'message': str(e)})
			response.status_code = 403
			return response
		else:
			return schema.dump(query).data, 201
