from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.romance.RomanceDao import RomanceDao

romanceapi = Blueprint('romanceapi', __name__)

# Trae todos los libros de romance
@romanceapi.route('/romance', methods=['GET'])
def getLibrosRomance():
    dao = RomanceDao()

    try:
        libros = dao.getTodos()

        return jsonify({
            'success': True,
            'data': libros,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener libros de romance: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@romanceapi.route('/romance/<int:id_libro>', methods=['GET'])
def getLibroRomance(id_libro):
    dao = RomanceDao()

    try:
        libro = dao.getPorId(id_libro)

        if libro:
            return jsonify({
                'success': True,
                'data': libro,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el libro con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener libro de romance: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo libro de romance
@romanceapi.route('/romance', methods=['POST'])
def addLibroRomance():
    data = request.get_json()
    dao = RomanceDao()

    campos_requeridos = ['titulo', 'descripcion', 'precio', 'imagen']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        titulo = data['titulo']
        descripcion = data['descripcion']
        precio = float(data['precio'])
        imagen = data['imagen']

        id_nuevo = dao.insertarLibro(titulo, descripcion, precio, imagen)

        if id_nuevo is not None:
            return jsonify({
                'success': True,
                'data': {'id': id_nuevo, 'titulo': titulo},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el libro. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar libro de romance: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@romanceapi.route('/romance/<int:id_libro>', methods=['PUT'])
def updateLibroRomance(id_libro):
    data = request.get_json()
    dao = RomanceDao()

    campos_requeridos = ['titulo', 'descripcion', 'precio', 'imagen']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        actualizado = dao.actualizarLibro(
            id_libro,
            data['titulo'],
            data['descripcion'],
            float(data['precio']),
            data['imagen']
        )

        if actualizado:
            return jsonify({
                'success': True,
                'data': {'id': id_libro},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el libro con el ID proporcionado o no se pudo actualizar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al actualizar libro de romance: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@romanceapi.route('/romance/<int:id_libro>', methods=['DELETE'])
def deleteLibroRomance(id_libro):
    dao = RomanceDao()

    try:
        eliminado = dao.eliminarLibro(id_libro)

        if eliminado:
            return jsonify({
                'success': True,
                'mensaje': f'Libro con ID {id_libro} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el libro con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar libro de romance: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
