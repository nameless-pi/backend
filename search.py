import re
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from sala_model import Sala
from usuario_model import Usuario, UsuarioSchema
from acesso_model import DireitoAcesso


user_schema = UsuarioSchema()


class SearchUsuario(Resource):
	@jwt_required()
	def post(self):
		regex = "[^\w\d]"
		parser = reqparse.RequestParser()

		parser.add_argument("query", type=str, location="json")
		parser.add_argument("filter", type=str, location="json")
		args = parser.parse_args(strict=True)

		if re.findall(regex, args["query"]):
			return None, 404

		if args["filter"] == "Tipo":
			usuario_list = Usuario.query.filter(
				Usuario.alive,
				Usuario.tipo.like("{}%".format(args["query"]))
			).all()
		elif args["filter"] == "Nome":
			usuario_list = Usuario.query.filter(
				Usuario.alive,
				Usuario.nome.like("{}%".format(args["query"]))
			).all()
		elif args["filter"] == "Sala":
			id_sala = Sala.query.filter(Sala.nome == args["query"]).first()
			if id_sala:
				id_sala = id_sala.id
			else:
				return None, 404
			acessos = DireitoAcesso.query.filter(
				DireitoAcesso.alive,
				DireitoAcesso.id_sala == id_sala
			).all()
			usuario_list = []
			for acesso in acessos:
				user = Usuario.query.filter(
					Usuario.alive,
					Usuario.id == acesso.id_usuario
				).first()
				user = {
					"id": getattr(user, "id"),
					"nome": getattr(user, "nome"),
					"tipo": getattr(user, "tipo"),
					"email": getattr(user, "email"),
					"rfid": getattr(user, "rfid"),
					"direito_acesso": [acesso],
					"last_update": getattr(user, "last_update"),
					"alive": getattr(user, "alive")
				}
				usuario_list.append(user)

		return user_schema.dump(usuario_list, many=True).data
