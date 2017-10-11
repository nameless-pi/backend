from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from admin_model import Admin, AdminSchema

schema = AdminSchema()


class AdminResource(Resource):
	@jwt_required()
	def get(self, id):
		pass

	@jwt_required()
	def put(self, id):
		pass

	@jwt_required()
	def delete(self, id):
		try:
			admin = Admin.query.get(id)
			if not admin:
				response = jsonify({"message": "Admin {} não existe".format(id)})
				response.status_code = 404
				return response
			admin.delete(admin)
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204


class AdminListResource(Resource):
	@jwt_required()
	def get(self):
		try:
			admins = Admin.query.all()
		except SQLAlchemyError as e:
			db.session.rollback()
			response = jsonify({"message": str(e)})
			response.status_code = 403
			return response
		else:
			return schema.dump(admins, many=True).data, 200

	# @jwt_required()
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location="json")
		parser.add_argument("login", type=str, required=True, location="json")
		parser.add_argument("senha", type=str, required=True, location="json")

		args = parser.parse_args(strict=True)

		try:
			admin = Admin(args["nome"], args["login"], args["senha"])
			admin.add(admin)
			query = Admin.query.get(admin.id)
		except SQLAlchemyError as e:
			db.session.rollback()
			response = jsonify({"message": str(e)})
			response.status_code = 403
			return response
		else:
			return schema.dump(query).data, 201
