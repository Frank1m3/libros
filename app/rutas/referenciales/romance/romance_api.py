from flask import Blueprint, render_template, Response, url_for, abort
from app.dao.referenciales.romance.RomanceDao import RomanceDao

# Definir el blueprint
romanceapi = Blueprint('romanceapi', __name__, template_folder='templates')

@romanceapi.route('/romance')
def romance_index():
    dao = RomanceDao()
    libros = dao.get_todos()
    
    for libro in libros:
        if 'id' in libro:
            libro['imagen_url'] = url_for('romanceapi.obtener_imagen', id_libro=libro['id'])
        else:
            libro['imagen_url'] = url_for('static', filename='fotos/default.jpg')  # Imagen por defecto
    return render_template('romance_index.html', libros=libros)

@romanceapi.route('/romance/<int:id_libro>')
def romance_detalle(id_libro):
    dao = RomanceDao()
    libro = dao.get_por_id(id_libro)
    
    if not libro:
        abort(404, "Libro no encontrado")

    libro['imagen_url'] = url_for('romanceapi.obtener_imagen', id_libro=id_libro)
    return render_template('romance_detalle.html', libro=libro)

@romanceapi.route('/romance/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = RomanceDao()
    fila = dao.obtener_imagen(id_libro)

    if not fila or not fila[1]:
        abort(404, "Imagen no encontrada")

    return Response(fila[1], mimetype='image/jpg')  # o 'image/png' según tu formato real
