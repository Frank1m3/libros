from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.idioma.IdiomaDao import IdiomaDao  # ajusta la ruta si es necesario

idiomaapi = Blueprint('idiomaapi', __name__)

@idiomaapi.route('/idiomas', methods=['GET'])
def getIdiomas():
    idiomadao = IdiomaDao()
    try:
        idiomas = idiomadao.getIdiomas()
        return jsonify({
            'success': True,
            'data': idiomas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los idiomas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@idiomaapi.route('/idiomas/<int:idioma_id>', methods=['GET'])
def getIdioma(idioma_id):
    idiomadao = IdiomaDao()
    try:
        idioma = idiomadao.getIdiomaById(idioma_id)
        if idioma:
            return jsonify({
                'success': True,
                'data': idioma,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el idioma con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener idioma: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@idiomaapi.route('/idiomas', methods=['POST'])
def addIdioma():
    data = request.get_json()
    idiomadao = IdiomaDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo nombre es obligatorio y no puede estar vacío.'
        }), 400

    try:
        nombre = data['nombre'].strip().upper()
        idioma_id = idiomadao.guardarIdioma(nombre)
        if idioma_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': idioma_id, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el idioma. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar idioma: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@idiomaapi.route('/idiomas/<int:idioma_id>', methods=['PUT'])
def updateIdioma(idioma_id):
    data = request.get_json()
    idiomadao = IdiomaDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo nombre es obligatorio y no puede estar vacío.'
        }), 400

    try:
        nombre = data['nombre'].strip().upper()
        if idiomadao.updateIdioma(idioma_id, nombre):
            return jsonify({
                'success': True,
                'data': {'id': idioma_id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el idioma con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar idioma: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@idiomaapi.route('/idiomas/<int:idioma_id>', methods=['DELETE'])
def deleteIdioma(idioma_id):
    idiomadao = IdiomaDao()
    try:
        if idiomadao.deleteIdioma(idioma_id):
            return jsonify({
                'success': True,
                'mensaje': f'Idioma con ID {idioma_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el idioma con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar idioma: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
