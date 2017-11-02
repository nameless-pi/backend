from flask import jsonify
from flask_restful import Resource, reqparse
import dateutil.parser

from setup import db
from horario_model import Horario, HorarioSchema
from sala_model import Sala, SalaSchema

schema = HorarioSchema()
schema2 = SalaSchema()

class RaspHorarioResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("last_update", type=str, required=True, location="json")
        parser.add_argument("sala", type=str, required=True, location="json")
        args = parser.parse_args(strict=True)

        sala = args["sala"]
        hora = dateutil.parser.parse(args["last_update"])

        sala_query = Sala.query.filter(Sala.nome == sala).first()
        salas = schema2.dump(sala_query).data
        id_sala = salas["id"]
        
        results = {}
        horario_query = Horario.query.filter(Horario.last_update > hora).filter(Horario.alive == True).filter(Horario.id_sala == id_sala)
        horarios = schema.dump(horario_query, many=True).data
        results_novos = []
        for h in horarios:
            adicionar = {}
            adicionar.update({"dia":h["dia"]})
            adicionar.update({"hora_inicio":h["hora_inicio"]})
            adicionar.update({"hora_fim":h["hora_fim"]})
            adicionar.update({"tipo_usuario":h["tipo_user"]})
            adicionar.update({"last_update":h["last_update"]})
            results_novos.append(adicionar)
        results.update({"novos": results_novos})

        horario_query = Horario.query.filter(Horario.last_update > hora).filter(Horario.alive == False).filter(Horario.id_sala == id_sala)
        horarios = schema.dump(horario_query, many=True).data
        results_removidos = []
        for h in horarios:
            adicionar = {}
            adicionar.update({"dia":h["dia"]})
            adicionar.update({"hora_inicio":h["hora_inicio"]})
            adicionar.update({"hora_fim":h["hora_fim"]})
            adicionar.update({"tipo_usuario":h["tipo_user"]})
            results_removidos.append(adicionar)
        results.update({"removidos": results_removidos})

        return jsonify(results)