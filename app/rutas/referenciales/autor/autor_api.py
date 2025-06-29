from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.autor.AutorDao import AutorDao  # ajusta la ruta si es necesario

autorapi = Blueprint('autorapi', __name__)

@autorapi.route('/autores', methods=['GET'])
def getAutores():
    autordao = AutorDao()
    try:
        autores = autordao.getAutores()
        return jsonify({
            'success': True,
            'data': autores,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los autores: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@autorapi.route('/autores/<int:autor_id>', methods=['GET'])
def getAutor(autor_id):
    autordao = AutorDao()
    try:
        autor = autordao.getAutorById(autor_id)
        if autor:
            return jsonify({
                'success': True,
                'data': autor,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el autor con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener autor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@autorapi.route('/autores', methods=['POST'])
def addAutor():
    data = request.get_json()
    autordao = AutorDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo nombre es obligatorio y no puede estar vacío.'
        }), 400

    try:
        nombre = data['nombre'].strip().upper()
        autor_id = autordao.guardarAutor(nombre)
        if autor_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': autor_id, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el autor. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar autor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@autorapi.route('/autores/<int:autor_id>', methods=['PUT'])
def updateAutor(autor_id):
    data = request.get_json()
    autordao = AutorDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo nombre es obligatorio y no puede estar vacío.'
        }), 400

    try:
        nombre = data['nombre'].strip().upper()
        if autordao.updateAutor(autor_id, nombre):
            return jsonify({
                'success': True,
                'data': {'id': autor_id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el autor con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar autor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@autorapi.route('/autores/<int:autor_id>', methods=['DELETE'])
def deleteAutor(autor_id):
    autordao = AutorDao()
    try:
        if autordao.deleteAutor(autor_id):
            return jsonify({
                'success': True,
                'mensaje': f'Autor con ID {autor_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el autor con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar autor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
