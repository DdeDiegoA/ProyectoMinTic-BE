from flask import jsonify, request, Blueprint
from controllers.resultado_controller import ResultadoController

#lo establecemos como app de blue print (coleccion de rutas)
resultado_Module = Blueprint('resultado',__name__)

#establecemos el controlador
controller = ResultadoController()

@resultado_Module.get('/') #aca tenemos el listar
def get_resultado():
    return jsonify(controller.get())

@resultado_Module.post('/') #Crear
def createResultado():
    result = controller.create(request.get_json())
    return jsonify(result), 201

@resultado_Module.get('/<string:id>') #listar por ID
def ver_resultado(id):
    return jsonify(controller.getById(id))


@resultado_Module.put('/<string:id>')#actualizar
def upd_resultado(id):
    controller.update(id, request.get_json())
    return jsonify({}), 204


@resultado_Module.delete('/<string:id>')#eliminar
def del_resultado(id):
    controller.delete(id)
    return jsonify({}), 204