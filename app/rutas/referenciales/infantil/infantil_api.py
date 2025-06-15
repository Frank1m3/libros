from flask import Blueprint, render_template, Response, url_for, abort
from app.dao.referenciales.infantiles.InfantilDao import InfantilDao

# Definir el blueprint
infantilapi = Blueprint('infantilapi', __name__, template_folder='templates')

@infantilapi.route('/infantil')
def infantil_index():
    dao = InfantilDao()
    libros = dao.get_todos()  # ← Corregido aquí
    
    for libro in libros:
        if 'id' in libro:
            libro['imagen_url'] = url_for('infantilapi.obtener_imagen', id_libro=libro['id'])
        else:
            libro['imagen_url'] = url_for('static', filename='fotos/default.jpg')  # Imagen por defecto
    return render_template('infantil_index.html', libros=libros)

@infantilapi.route('/infantil/<int:id_libro>')
def infantil_detalle(id_libro):
    dao = InfantilDao()
    libro = dao.get_por_id(id_libro)
    
    if not libro:
        abort(404, "Libro no encontrado")

    libro['imagen_url'] = url_for('infantilapi.obtener_imagen', id_libro=id_libro)
    return render_template('infantil_detalle.html', libro=libro)

@infantilapi.route('/infantil/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = InfantilDao()
    fila = dao.obtener_imagen(id_libro)

    if not fila or not fila[1]:
        abort(404, "Imagen no encontrada")

    return Response(fila[1], mimetype='image/jpg')  # o 'image/png' según tu formato real
