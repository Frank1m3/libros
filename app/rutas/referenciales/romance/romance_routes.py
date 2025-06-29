from flask import Blueprint, render_template, abort, request, jsonify, url_for, Response
from app.dao.referenciales.romance.RomanceDao import RomanceDao

rommod = Blueprint('romance', __name__, template_folder='templates')

@rommod.route('/romance-index')
def romanceIndex():
    dao = RomanceDao()
    libros = dao.get_todos()
    # Agregar url de imagen para cada libro
    for libro in libros:
        libro['imagen_url'] = url_for('romanceapi.obtener_imagen', id_libro=libro['id'])
    return render_template('romance-index.html', libros=libros)

@rommod.route('/romance-detalle/<int:id_libro>')
def romanceDetalle(id_libro):
    dao = RomanceDao()
    libro = dao.get_por_id(id_libro)
    if libro:
        # agregar url imagen para detalle
        libro['imagen_url'] = url_for('romanceapi.obtener_imagen', id_libro=id_libro)
        return render_template('romance-detalle.html', libro=libro)
    else:
        return render_template('romance-no_encontrado.html'), 404

# Endpoint para la imagen
@rommod.route('/imagen/<int:id_libro>')
def obtener_imagen(id_libro):
    dao = RomanceDao()
    resultado = dao.obtener_imagen(id_libro)
    if not resultado or not resultado[1]:
        abort(404)
    return Response(resultado[1], mimetype='image/jpeg')

# Endpoint AJAX para búsqueda de libros (devuelve JSON)
@rommod.route('/buscar-libros')
def buscar_libros():
    q = request.args.get('q', '').strip().lower()
    dao = RomanceDao()
    resultados = dao.buscar_por_titulo(q)

    salida = []
    for libro in resultados:
        salida.append({
            'id': libro.get('id'),
            'titulo': libro.get('titulo'),
            'autor': libro.get('autor') or 'Desconocido',
            'url_detalle': url_for('romance.romanceDetalle', id_libro=libro.get('id'))
        })
    return jsonify(salida)
