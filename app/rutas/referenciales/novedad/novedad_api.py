from flask import Blueprint, render_template, Response, url_for, abort, jsonify, request
from app.dao.referenciales.novedades.NovedadDao import NovedadDao

# Definir el blueprint
novedadapi = Blueprint('novedadapi', __name__, template_folder='templates')

# Ruta principal: mostrar todos los libros de novedades
@novedadapi.route('/novedades')
def novedad_index():
    dao = NovedadDao()
    libros = dao.get_todos()

    for libro in libros:
        libro['imagen_url'] = (
            url_for('novedadapi.obtener_imagen', id_libro=libro['id'])
            if 'id' in libro else url_for('static', filename='fotos/default.jpg')
        )
    
    return render_template('novedades_index.html', libros=libros)

# Ruta de detalle por ID de libro
@novedadapi.route('/novedades/<int:id_libro>')
def novedad_detalle(id_libro):
    dao = NovedadDao()
    libro = dao.get_por_id(id_libro)

    if not libro:
        abort(404, "Libro no encontrado")

    libro['imagen_url'] = url_for('novedadapi.obtener_imagen', id_libro=id_libro)
    return render_template('novedades_detalle.html', libro=libro)

# Ruta para obtener la imagen del libro
@novedadapi.route('/novedades/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = NovedadDao()
    fila = dao.obtener_imagen(id_libro)

    if not fila or not fila[1]:
        abort(404, "Imagen no encontrada")

    return Response(fila[1], mimetype='image/jpg')

# Ruta AJAX para buscar libros por título usando DAO (más eficiente)
@novedadapi.route('/novedades/buscar-libros')
def buscar_libros():
    query = request.args.get('q', '').strip()
    dao = NovedadDao()
    resultados = []

    if query:
        libros = dao.buscar_por_titulo(query)
        for libro in libros:
            resultados.append({
                'id': libro['id'],
                'titulo': libro['titulo'],
                'autor': libro.get('autor', 'Autor desconocido')
            })

    return jsonify(resultados)
