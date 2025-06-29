from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.categoria.CategoriaDao import CategoriaDao  # ajusta la ruta si cambia

categoriaapi = Blueprint('categoriaapi', __name__)

@categoriaapi.route('/categorias', methods=['GET'])
def getCategorias():
    dao = CategoriaDao()
    try:
        categorias = dao.getCategorias()
        return jsonify({
            'success': True,
            'data': categorias,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener categorías: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al obtener categorías.'
        }), 500

@categoriaapi.route('/categorias/<int:id>', methods=['GET'])
def getCategoria(id):
    dao = CategoriaDao()
    try:
        categoria = dao.getCategoriaById(id)
        if categoria:
            return jsonify({
                'success': True,
                'data': categoria,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la categoría.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener categoría por ID: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno.'
        }), 500

@categoriaapi.route('/categorias', methods=['POST'])
def addCategoria():
    data = request.get_json()
    dao = CategoriaDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo nombre es obligatorio.'
        }), 400

    try:
        nombre = data['nombre'].strip().upper()
        id_categoria = dao.guardarCategoria(nombre)
        if id_categoria is not None:
            return jsonify({
                'success': True,
                'data': {'id': id_categoria, 'nombre': nombre},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la categoría.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al guardar categoría: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al guardar.'
        }), 500

@categoriaapi.route('/categorias/<int:id>', methods=['PUT'])
def updateCategoria(id):
    data = request.get_json()
    dao = CategoriaDao()

    if not data or 'nombre' not in data or not data['nombre'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo nombre es obligatorio.'
        }), 400

    try:
        nombre = data['nombre'].strip().upper()
        if dao.updateCategoria(id, nombre):
            return jsonify({
                'success': True,
                'data': {'id': id, 'nombre': nombre},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la categoría o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar categoría: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al actualizar.'
        }), 500

@categoriaapi.route('/categorias/<int:id>', methods=['DELETE'])
def deleteCategoria(id):
    dao = CategoriaDao()
    try:
        if dao.deleteCategoria(id):
            return jsonify({
                'success': True,
                'mensaje': f'Categoría con ID {id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la categoría o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar categoría: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al eliminar.'
        }), 500
