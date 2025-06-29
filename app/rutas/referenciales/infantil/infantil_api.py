from flask import Blueprint, render_template, Response, url_for, abort, jsonify, request
from app.dao.referenciales.infantiles.InfantilDao import InfantilDao

# Definir el blueprint
infantilapi = Blueprint('infantilapi', __name__, template_folder='templates')

# Ruta principal: mostrar todos los libros infantiles
@infantilapi.route('/infantil')
def infantil_index():
    dao = InfantilDao()
    libros = dao.get_todos()

    for libro in libros:
        libro['imagen_url'] = (
            url_for('infantilapi.obtener_imagen', id_libro=libro['id'])
            if 'id' in libro else url_for('static', filename='fotos/default.jpg')
        )
    
    return render_template('infantil_index.html', libros=libros)

# Ruta de detalle por ID de libro
@infantilapi.route('/infantil/<int:id_libro>')
def infantil_detalle(id_libro):
    dao = InfantilDao()
    libro = dao.get_por_id(id_libro)

    if not libro:
        abort(404, "Libro no encontrado")

    libro['imagen_url'] = url_for('infantilapi.obtener_imagen', id_libro=id_libro)
    return render_template('infantil_detalle.html', libro=libro)

# Ruta para obtener la imagen del libro
@infantilapi.route('/infantil/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = InfantilDao()
    fila = dao.obtener_imagen(id_libro)

    if not fila or not fila[1]:
        abort(404, "Imagen no encontrada")

    return Response(fila[1], mimetype='image/jpg')

# Ruta AJAX para buscar libros por título usando DAO (más eficiente)
@infantilapi.route('/infantil/buscar-libros')
def buscar_libros():
    query = request.args.get('q', '').strip()
    dao = InfantilDao()
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
