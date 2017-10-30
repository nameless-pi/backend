from flask import jsonify
from flask_restful import Resource, reqparse
import dateutil.parser

from setup import db
from acesso_model import DireitoAcesso, AcessoSchema, AcessoSchemaRasp
from usuario_model import Usuario, UsuarioSchema

schema = AcessoSchemaRasp()
schema2 = UsuarioSchema()

class RaspRfidResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("last_update", type=str, required=True, location="json")
        parser.add_argument("sala", type=str, required=True, location="json")
        args = parser.parse_args(strict=True)

        sala = args["sala"]
        hora = dateutil.parser.parse(args["last_update"])
        print(hora)

        # direto_acesso_query = DireitoAcesso.query.all()
        # results = schema.dump(direto_acesso_query, many=True).data
        # results2 =[]
        # for r in results:
        #     if r["nome_sala"] == sala:
        #         results2.append(r)
        
        usuario_query = Usuario.query.all()
        usuarios = schema2.dump(usuario_query, many=True).data
        # print(usuarios)
        results = []
        for u in usuarios:
            for d in u["direito_acesso"]:
                if (d["nome_sala"] == sala) and (dateutil.parser.parse(u["last_update"]) > hora):
                    adicionar = {}
                    adicionar.update({"rfid":u["rfid"]})
                    adicionar.update({"tipo":u["tipo"]})
                    results.append(adicionar)
                    adicionar = {}
        # print(results)
        # print("\n")
        
        return jsonify(results)