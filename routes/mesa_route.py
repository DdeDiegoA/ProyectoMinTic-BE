from flask import jsonify, request, Blueprint
from controllers.mesa_controller import MesaController

#lo establecemos como app de blue print (coleccion de rutas)
mesa_Module = Blueprint('mesa',__name__)

#establecemos el controlador
controller = MesaController()

@mesa_Module.get('/') #aca tenemos el listar
def get_mesas():
    return jsonify(controller.get())

@mesa_Module.post('/') #Crear
def createMesas():
    result = controller.create(request.get_json())
    return jsonify(result), 201


@mesa_Module.get('/<string:id>') #listar por ID
def ver_mesa(id):
    return jsonify(controller.getById(id))


@mesa_Module.put('/<string:id>')#actualizar
def upd_mesa(id):
    controller.update(id, request.get_json())
    return jsonify({}), 204


@mesa_Module.delete('/<string:id>')#eliminar
def del_mesa(id):
    controller.delete(id)
    return jsonify({}), 204
