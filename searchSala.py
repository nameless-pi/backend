import re
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from sala_model import Sala, SalaSchema
from horario_model import Horario

Sala_schema = SalaSchema()

class SearchSala(Resource):

    @jwt_required()
    def post(self):
        regex = "[^\w\d]"

        parser = reqparse.RequestParser()

        parser.add_argument("query", type=str, location="json")
        parser.add_argument("filter", type=str, location="json")

        args = parser.parse_args(strict=True)

        if re.findall(regex, args["query"]):
            return None, 404

        if args["filter"] == "Dia":
            horarios = Horario.query.filter(Horario.alive == True, 
                                          Horario.dia.like("{}%".format(args["query"])))
            salas = []
            for horario in horarios:
                sala = Sala.query.filter(Sala.alive == True, Sala.id == horario.id_sala).first()
                sala = {"id": getattr(sala, "id"), 
						"nome": getattr(sala, "nome"), 
						"horarios": getattr(sala, "horarios")
						}
                salas.append(sala)
        else:
            return None, 404

        if  salas == []:
            return None, 404

        return Sala_schema.dump(salas, many=True).data
