from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.novedades.NovedadDao import NovedadDao

novedadapi = Blueprint('novedadapi', __name__)

@novedadapi.route('/novedades', methods=['GET'])
def getNovedades():
    dao = NovedadDao()
    try:
        data = dao.getTodos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener novedades: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno.'}), 500

@novedadapi.route('/novedades/<int:id_libro>', methods=['GET'])
def getNovedad(id_libro):
    dao = NovedadDao()
    try:
        libro = dao.getPorId(id_libro)
        if libro:
            return jsonify({'success': True, 'data': libro, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'Libro no encontrado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener novedad: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno.'}), 500

@novedadapi.route('/novedades', methods=['POST'])
def addNovedad():
    data = request.get_json()
    campos = ['titulo', 'descripcion', 'precio', 'imagen']
    
    for campo in campos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'Campo {campo} es obligatorio'}), 400

    dao = NovedadDao()
    try:
        id_libro = dao.insertarLibro(data['titulo'], data['descripcion'], data['precio'], data['imagen'])
        if id_libro:
            return jsonify({'success': True, 'data': {'id': id_libro}, 'error': None}), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo insertar.'}), 500
    except Exception as e:
        app.logger.error(f"Error al insertar novedad: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno.'}), 500

@novedadapi.route('/novedades/<int:id_libro>', methods=['PUT'])
def updateNovedad(id_libro):
    data = request.get_json()
    campos = ['titulo', 'descripcion', 'precio', 'imagen']

    for campo in campos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'Campo {campo} es obligatorio'}), 400

    dao = NovedadDao()
    try:
        if dao.actualizarLibro(id_libro, data['titulo'], data['descripcion'], data['precio'], data['imagen']):
            return jsonify({'success': True, 'data': {'id': id_libro}, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar o no existe.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar novedad: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno.'}), 500

@novedadapi.route('/novedades/<int:id_libro>', methods=['DELETE'])
def deleteNovedad(id_libro):
    dao = NovedadDao()
    try:
        if dao.eliminarLibro(id_libro):
            return jsonify({'success': True, 'mensaje': 'Eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el libro o no se pudo eliminar.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar novedad: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno.'}), 500
