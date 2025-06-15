from flask import Blueprint, render_template, Response, url_for, abort
from app.dao.referenciales.registrar.RegistrarDao import RegistrarDao


registrarapi = Blueprint('registrarapi', __name__, template_folder='templates')

@registrarapi.route('/registrar')
def registrar_index():
    dao = RegistrarDao()
    libros = dao.get_todos()
    
    for libro in libros:
        if 'id' in libro:
            libro['imagen_url'] = url_for('registrarapi.obtener_imagen', libro_id=libro['id'])
        else:
            libro['imagen_url'] = url_for('static', filename='fotos/default.jpg')
    return render_template('registrar_index.html', libros=libros)

@registrarapi.route('/registrar/<int:libro_id>')
def registrar_detalle(libro_id):
    dao = RegistrarDao()
    libro = dao.obtener_libro_por_id(libro_id)
    
    if not libro:
        abort(404, "Libro no encontrado")

    libro['imagen_url'] = url_for('registrarapi.obtener_imagen', libro_id=libro_id)
    return render_template('registrar_detalle.html', libro=libro)

@registrarapi.route('/registrar/imagen/<int:libro_id>')
def obtener_imagen(libro_id):
    dao = RegistrarDao()
    imagen = dao.obtener_imagen(libro_id)

    if not imagen:
        abort(404, "Imagen no encontrada")

    return Response(imagen, mimetype='image/jpg')
