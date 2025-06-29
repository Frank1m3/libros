from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tomo.TomoDao import TomoDao

tomoapi = Blueprint('tomoapi', __name__)

@tomoapi.route('/tomos', methods=['GET'])
def getTomos():
    dao = TomoDao()
    try:
        data = dao.getTomos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tomos: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@tomoapi.route('/tomos/<int:tomo_id>', methods=['GET'])
def getTomo(tomo_id):
    dao = TomoDao()
    try:
        tomo = dao.getTomoById(tomo_id)
        if tomo:
            return jsonify({'success': True, 'data': tomo, 'error': None}), 200
        return jsonify({'success': False, 'error': 'Tomo no encontrado'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener tomo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@tomoapi.route('/tomos', methods=['POST'])
def addTomo():
    data = request.get_json()
    dao = TomoDao()

    if not data or 'numero' not in data:
        return jsonify({'success': False, 'error': 'Número es obligatorio'}), 400

    numero = int(data['numero'])
    descripcion = data.get('descripcion', '').strip()

    try:
        tomo_id = dao.guardarTomo(numero, descripcion)
        if tomo_id:
            return jsonify({'success': True, 'data': {'id': tomo_id, 'numero': numero, 'descripcion': descripcion}, 'error': None}), 201
        return jsonify({'success': False, 'error': 'No se pudo guardar el tomo'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar tomo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@tomoapi.route('/tomos/<int:tomo_id>', methods=['PUT'])
def updateTomo(tomo_id):
    data = request.get_json()
    dao = TomoDao()

    if not data or 'numero' not in data:
        return jsonify({'success': False, 'error': 'Número es obligatorio'}), 400

    numero = int(data['numero'])
    descripcion = data.get('descripcion', '').strip()

    try:
        if dao.updateTomo(tomo_id, numero, descripcion):
            return jsonify({'success': True, 'data': {'id': tomo_id, 'numero': numero, 'descripcion': descripcion}, 'error': None}), 200
        return jsonify({'success': False, 'error': 'Tomo no encontrado o no actualizado'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tomo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@tomoapi.route('/tomos/<int:tomo_id>', methods=['DELETE'])
def deleteTomo(tomo_id):
    dao = TomoDao()
    try:
        if dao.deleteTomo(tomo_id):
            return jsonify({'success': True, 'mensaje': 'Tomo eliminado', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se pudo eliminar'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar tomo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500
