from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from admin_model import Admin, AdminSchema

schema = AdminSchema()


def send_message(message, status_code):
	response = jsonify({"message": message})
	response.status_code = status_code
	return response


class AdminResource(Resource):
	#@jwt_required()
	def get(self, id):
		pass

	#@jwt_required()
	def put(self, id):
		parser = reqparse.RequestParser()

		parser.add_argument("login", type=str, location="json")
		parser.add_argument("nome", type=str, location="json")
		parser.add_argument("new_password", type=str, location="json")
		parser.add_argument("current_password", type=str, location="json")

		args = parser.parse_args(strict=True)
		admin = Admin.query.get(id)

		if not admin:
			return send_message("Administrador {} não existe".format(id), 404)
		else:
			if admin.verify_password(args["current_password"]):
				if args["new_password"]:
					admin.hash_password(args["new_password"])
			else:
				return send_message("Senha atual inválida".format(id), 412)

		if args["nome"]:
			admin.nome = args["nome"]
		if args["login"] and admin.login != args["login"]:
			check_login = len(db.session.query(Admin).filter(Admin.login == args["login"]).all()) == 1
			if not check_login:
				admin.login = args["login"]
			else:
				return send_message("Este login já existe".format(id), 403)
		admin.update()
		return schema.dump(admin).data, 200

	#@jwt_required()
	def delete(self, id):
		try:
			admin = Admin.query.get(id)
			if not admin:
				return send_message("Administrador {} não existe".format(id), 404)
			admin.delete(admin)
		except SQLAlchemyError as e:
			db.session.rollback()
			return send_message(str(e), 403)
		else:
			return None, 204


class AdminListResource(Resource):
	@jwt_required()
	def get(self):
		try:
			admins = Admin.query.all()
		except SQLAlchemyError as e:
			db.session.rollback()
			return send_message(str(e), 403)
		else:
			return schema.dump(admins, many=True).data, 200

	# @jwt_required()
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location="json")
		parser.add_argument("login", type=str, required=True, location="json")
		parser.add_argument("password", type=str, required=True, location="json")

		args = parser.parse_args(strict=True)

		try:
			admin = Admin(args["nome"], args["login"], args["password"])
			admin.add(admin)
			query = Admin.query.get(admin.id)
		except SQLAlchemyError as e:
			db.session.rollback()
			return send_message(str(e), 403)
		else:
			return schema.dump(query).data, 201
