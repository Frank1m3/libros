import os
from flask import Blueprint, render_template, redirect, url_for, Response, abort, request, jsonify
from app.dao.referenciales.novedades.NovedadDao import NovedadDao

# Crear blueprint, sin indicar template_folder para usar la carpeta global "templates"
novmod = Blueprint('novedad', __name__)

# Ruta para la página principal de libros novedades
@novmod.route('/novedad-index')
def novedadIndex():
    dao = NovedadDao()
    libros = dao.get_todos()  # Obtener todos los libros novedades
    
    # Agregar URL para la imagen de cada libro
    for libro in libros:
        libro['imagen_url'] = url_for('novedad.obtener_imagen', id_libro=libro['id'])
    
    # Renderizar plantilla ubicada en templates/novedad-index.html
    return render_template('novedad-index.html', libros=libros)

# Ruta para ver detalle de un libro novedad por id
@novmod.route('/novedad-detalle/<int:id_libro>')
def novedadDetalle(id_libro):
    dao = NovedadDao()
    libro = dao.get_por_id(id_libro)
    if not libro:
        abort(404)  # Si no existe, 404
    
    # Agregar URL para la imagen del libro
    libro['imagen_url'] = url_for('novedad.obtener_imagen', id_libro=id_libro)
    
    # Renderizar plantilla templates/novedad-detalle.html
    return render_template('novedad-detalle.html', libro=libro)

# Ruta para servir la imagen del libro
@novmod.route('/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = NovedadDao()
    resultado = dao.obtener_imagen(id_libro)  # Debe retornar algo como (id, imagen_bytes)
    if not resultado or not resultado[1]:
        abort(404)
    
    # Retornar la imagen con el mimetype adecuado
    return Response(resultado[1], mimetype='image/jpeg')

# Ruta para página de contactos (opcional, puede ir a otro blueprint)
@novmod.route('/contactos')
def contactos():
    return render_template('contactos.html')

# Ruta para búsqueda AJAX de libros por título
@novmod.route('/buscar-libros')
def buscar_libros():
    q = request.args.get('q', '').strip().lower()
    dao = NovedadDao()
    resultados = dao.buscar_por_titulo(q)  # Método del DAO que retorna lista de dicts

    salida = []
    for libro in resultados:
        salida.append({
            'id': libro.get('id'),
            'titulo': libro.get('titulo'),
            'autor': libro.get('autor', 'Desconocido'),
            'url_detalle': url_for('novedad.novedadDetalle', id_libro=libro.get('id'))
        })

    return jsonify(salida)
