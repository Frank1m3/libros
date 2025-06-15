from flask import Blueprint, request, jsonify
from app.dao.contactos.ContactoDao import ContactoDao

contactoapi = Blueprint('contactoapi', __name__)

# Ruta para insertar un contacto vía API (JSON)
@contactoapi.route('/contactos', methods=['POST'])
def api_insertar_contacto():
    data = request.get_json()

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    telefono = data.get('telefono')
    mensaje = data.get('mensaje')

    if not all([nombre, apellido, correo, telefono, mensaje]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    dao = ContactoDao()  # crear instancia
    try:
        exito = dao.insertar(nombre, apellido, correo, telefono, mensaje)
        if exito:
            return jsonify({'mensaje': 'Mensaje guardado correctamente'}), 201
        else:
            return jsonify({'error': 'Error al guardar el mensaje'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
