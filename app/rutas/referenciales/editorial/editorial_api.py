from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.editorial.EditorialDao import EditorialDao  # Ajustá ruta si es necesario

editorialapi = Blueprint('editorialapi', __name__)

@editorialapi.route('/editoriales', methods=['GET'])
def getEditoriales():
    dao = EditorialDao()
    try:
        data = dao.getEditoriales()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener editoriales: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@editorialapi.route('/editoriales/<int:editorial_id>', methods=['GET'])
def getEditorial(editorial_id):
    dao = EditorialDao()
    try:
        editorial = dao.getEditorialById(editorial_id)
        if editorial:
            return jsonify({'success': True, 'data': editorial, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'Editorial no encontrada'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener editorial: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@editorialapi.route('/editoriales', methods=['POST'])
def addEditorial():
    data = request.get_json()
    dao = EditorialDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({'success': False, 'error': 'Nombre obligatorio'}), 400

    try:
        nombre = data['nombre'].strip().upper()
        editorial_id = dao.guardarEditorial(nombre)
        if editorial_id is not None:
            return jsonify({'success': True, 'data': {'id': editorial_id, 'nombre': nombre}, 'error': None}), 201
        return jsonify({'success': False, 'error': 'No se pudo guardar'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar editorial: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@editorialapi.route('/editoriales/<int:editorial_id>', methods=['PUT'])
def updateEditorial(editorial_id):
    data = request.get_json()
    dao = EditorialDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({'success': False, 'error': 'Nombre obligatorio'}), 400

    try:
        nombre = data['nombre'].strip().upper()
        if dao.updateEditorial(editorial_id, nombre):
            return jsonify({'success': True, 'data': {'id': editorial_id, 'nombre': nombre}, 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró o no se actualizó'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar editorial: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500

@editorialapi.route('/editoriales/<int:editorial_id>', methods=['DELETE'])
def deleteEditorial(editorial_id):
    dao = EditorialDao()
    try:
        if dao.deleteEditorial(editorial_id):
            return jsonify({'success': True, 'mensaje': 'Eliminada correctamente', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se pudo eliminar'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar editorial: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500
