from flask import jsonify
from flask_restful import Resource, reqparse
import dateutil.parser

from setup import db
# from acesso_model import DireitoAcesso, AcessoSchema, AcessoSchemaRasp
from usuario_model import Usuario, UsuarioSchema

schema = UsuarioSchema()

class RaspRfidResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("last_update", type=str, required=True, location="json")
        parser.add_argument("sala", type=str, required=True, location="json")
        args = parser.parse_args(strict=True)

        sala = args["sala"]
        hora = dateutil.parser.parse(args["last_update"])
        
        results = {}
        usuario_query = Usuario.query.filter(Usuario.last_update > hora).filter(Usuario.alive == True)
        usuarios = schema.dump(usuario_query, many=True).data
        results_novos = []
        for u in usuarios:
            for d in u["direito_acesso"]:
                if (d["nome_sala"] == sala):
                    adicionar = {}
                    adicionar.update({"rfid":u["rfid"]})
                    adicionar.update({"tipo":u["tipo"]})
                    adicionar.update({"last_update":u["last_update"]})
                    results_novos.append(adicionar)
        results.update({"novos": results_novos})
        
        usuario_query = Usuario.query.filter(Usuario.last_update > hora).filter(Usuario.alive == False)
        usuarios = schema.dump(usuario_query, many=True).data
        results_removidos = []
        for u in usuarios:
            for d in u["direito_acesso"]:
                if (d["nome_sala"] == sala):
                    adicionar = {}
                    adicionar.update({"rfid":u["rfid"]})
                    results_removidos.append(adicionar)
        results.update({"removidos": results_removidos})

        return jsonify(results)