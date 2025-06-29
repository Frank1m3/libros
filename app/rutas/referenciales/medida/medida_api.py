from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.medida.MedidaDao import MedidaDao  # ajusta la ruta si es necesario

medidaapi = Blueprint('medidaapi', __name__)

@medidaapi.route('/medidas', methods=['GET'])
def getMedidas():
    medidadao = MedidaDao()
    try:
        medidas = medidadao.getMedidas()
        return jsonify({
            'success': True,
            'data': medidas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las medidas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@medidaapi.route('/medidas/<int:medida_id>', methods=['GET'])
def getMedida(medida_id):
    medidadao = MedidaDao()
    try:
        medida = medidadao.getMedidaById(medida_id)
        if medida:
            return jsonify({
                'success': True,
                'data': medida,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la medida con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener medida: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@medidaapi.route('/medidas', methods=['POST'])
def addMedida():
    data = request.get_json()
    medidadao = MedidaDao()

    # Validar que los campos existan, pueden ser None pero chequeamos la presencia
    alto = data.get('alto', None)
    ancho = data.get('ancho', None)
    profundidad = data.get('profundidad', None)

    try:
        medida_id = medidadao.guardarMedida(alto, ancho, profundidad)
        if medida_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': medida_id, 'alto': alto, 'ancho': ancho, 'profundidad': profundidad},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la medida. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar medida: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@medidaapi.route('/medidas/<int:medida_id>', methods=['PUT'])
def updateMedida(medida_id):
    data = request.get_json()
    medidadao = MedidaDao()

    alto = data.get('alto', None)
    ancho = data.get('ancho', None)
    profundidad = data.get('profundidad', None)

    try:
        if medidadao.updateMedida(medida_id, alto, ancho, profundidad):
            return jsonify({
                'success': True,
                'data': {'id': medida_id, 'alto': alto, 'ancho': ancho, 'profundidad': profundidad},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la medida con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar medida: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@medidaapi.route('/medidas/<int:medida_id>', methods=['DELETE'])
def deleteMedida(medida_id):
    medidadao = MedidaDao()
    try:
        if medidadao.deleteMedida(medida_id):
            return jsonify({
                'success': True,
                'mensaje': f'Medida con ID {medida_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la medida con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar medida: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
