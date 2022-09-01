from flask import jsonify, request, Blueprint
from controllers.partido_controller import PartidoController 

#lo establecemos como app de blue print (coleccion de rutas)
partido_Module = Blueprint('partido',__name__)

#establecemos el controlador
controller = PartidoController()

@partido_Module.get('/') #aca tenemos el listar
def get_partidos():
    return jsonify(controller.get())

@partido_Module.post('/') #Crear
def createPartido():
    result = controller.create(request.get_json())
    return jsonify(result), 201


@partido_Module.get('/<string:id>') #listar por ID
def ver_partido(id):
    return jsonify(controller.getById(id))


@partido_Module.put('/<string:id>')#actualizar
def upd_partido(id):
    controller.update(id, request.get_json())
    return jsonify({}), 204


@partido_Module.delete('/<string:id>')#eliminar
def del_partido(id):
    controller.delete(id)
    return jsonify({}), 204