from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.dao.contactos.ContactoDao import ContactoDao

contactomod = Blueprint('contactos', __name__, template_folder='templates')

@contactomod.route('/contactos', methods=['GET', 'POST'])
def vista_contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        mensaje = request.form.get('mensaje')

        # Validar que no haya campos vacíos (opcional)
        if not all([nombre, apellido, correo, telefono, mensaje]):
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('contactos.vista_contacto'))

        dao = ContactoDao()
        exito = dao.insertar(nombre, apellido, correo, telefono, mensaje)

        if exito:
            flash('Mensaje enviado correctamente.', 'success')
        else:
            flash('Error al enviar el mensaje.', 'danger')

        return redirect(url_for('contactos.vista_contacto'))

    return render_template('contactos.html')
