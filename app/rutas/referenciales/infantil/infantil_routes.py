import os
from flask import Blueprint, render_template, redirect, url_for, Response, abort,request,jsonify
from app.dao.referenciales.infantiles.InfantilDao import InfantilDao

# Crear blueprint, sin indicar template_folder para usar la carpeta global "templates"
infmod = Blueprint('infantil', __name__)

# Ruta para la página principal de libros infantiles
@infmod.route('/infantil-index')
def infantilIndex():
    dao = InfantilDao()
    libros = dao.get_todos()  # Obtener todos los libros infantiles
    
    # Agregar URL para la imagen de cada libro
    for libro in libros:
        libro['imagen_url'] = url_for('infantil.obtener_imagen', id_libro=libro['id'])
    
    # Renderizar plantilla ubicada en templates/infantil-index.html
    return render_template('infantil-index.html', libros=libros)

# Ruta para ver detalle de un libro infantil por id
@infmod.route('/infantil-detalle/<int:id_libro>')
def infantilDetalle(id_libro):
    dao = InfantilDao()
    libro = dao.get_por_id(id_libro)
    if not libro:
        abort(404)  # Si no existe, 404
    
    # Agregar URL para la imagen del libro
    libro['imagen_url'] = url_for('infantil.obtener_imagen', id_libro=id_libro)
    
    # Renderizar plantilla templates/infantil-detalle.html
    return render_template('infantil-detalle.html', libro=libro)

# Ruta para servir la imagen del libro
@infmod.route('/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = InfantilDao()
    resultado = dao.obtener_imagen(id_libro)  # Debe retornar algo como (id, imagen_bytes)
    if not resultado or not resultado[1]:
        abort(404)
    
    # Retornar la imagen con el mimetype adecuado
    return Response(resultado[1], mimetype='image/jpeg')

# Ruta para página de contactos (opcional, puede ir a otro blueprint)
@infmod.route('/contactos')
def contactos():
    return render_template('contactos.html')


@infmod.route('/buscar-libros')
def buscar_libros():
    q = request.args.get('q', '').lower()
    dao = InfantilDao()
    resultados = dao.buscar_por_titulo(q)  # Este método lo creás en tu DAO

    return jsonify(resultados)
