from setup import api, app
from admin_resource import AdminResource, AdminListResource
from sala_resource import SalaResource, SalaListResource, SalaHorarioResource
from usuario_resource import UsuarioResource, UsuarioListResource
from horario_resource import HorarioResource, HorarioListResource
from json_resource import JSONResource
from rasp_rfid_resource import RaspRfidResource
from rasp_horario_resource import RaspHorarioResource
from rasp_check_evento_resource import RaspCheckEventoResource
from rasp_evento_resource import RaspEventoResource

from search import SearchUsuario
from searchSala import SearchSala

prefix = "/api/v1"
api.add_resource(SearchUsuario, prefix + "/pesquisa")

api.add_resource(SearchSala, prefix + "/pesquisalas")

api.add_resource(AdminResource, prefix + "/admins/<int:id>")
api.add_resource(AdminListResource, prefix + "/admins")

api.add_resource(UsuarioResource, prefix + "/usuarios/<int:id>")
api.add_resource(UsuarioListResource, prefix + "/usuarios")

api.add_resource(SalaResource, prefix + "/salas/<int:id>")
api.add_resource(SalaListResource, prefix + "/salas")
api.add_resource(SalaHorarioResource, prefix + "/salas/horarios/<int:id>")

api.add_resource(HorarioResource, prefix + "/horarios/<int:id>")
api.add_resource(HorarioListResource, prefix + "/horarios")

api.add_resource(JSONResource, prefix + "/json/<string:tipo>")

api.add_resource(RaspRfidResource, prefix + "/rasp/rfid")
api.add_resource(RaspHorarioResource, prefix + "/rasp/horario")
api.add_resource(RaspCheckEventoResource, prefix + "/rasp/checkevento")
api.add_resource(RaspEventoResource, prefix + "/rasp/evento")

if __name__ == "__main__":
	app.run(
		host=app.config["HOST"],
		port=app.config["PORT"],
		debug=app.config["DEBUG"]
	)
