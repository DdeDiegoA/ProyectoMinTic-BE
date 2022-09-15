from flask import jsonify, request, Blueprint
from controllers.resultado_controller import ResultadoController

#lo establecemos como app de blue print (coleccion de rutas)
resultado_Module = Blueprint('resultado',__name__)

#establecemos el controlador
controller = ResultadoController()

@resultado_Module.get('/') #aca tenemos el listar
def get_resultado():
    #return jsonify(controller.get())
    #PUSE ESTO NUEVO
    return jsonify(controller.get(request.args))

@resultado_Module.post('/mesa/<string:mesa_id>/candidato/<string:candidato_id>') #Crear
def createResultado(mesa_id,candidato_id):
    result = controller.create(request.get_json(), mesa_id,candidato_id)
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

#total de votos para todos los candidatos
@resultado_Module.get('/total')
def get_total():
    return jsonify(controller.get_total())

#total de votos para un candidato
@resultado_Module.get('/totalCandidato/<string:candidato_id>')
def total_candidato(candidato_id):
    return jsonify(controller.total_candidato(candidato_id))

#total de votos para cada candidato por mesa
@resultado_Module.get('/totalMesa')
def get_total_mesa():
    return jsonify(controller.get_total_mesa())

@resultado_Module.get('/totalPartido')
def get_total_partido():
    return jsonify(controller.get_total_partido())






    