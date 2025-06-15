from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from app.dao.referenciales.registrar.RegistrarDao import RegistrarDao

# Define el blueprint con la carpeta templates para que Flask busque ahí
registrar = Blueprint('registrar', __name__, template_folder='templates')

@registrar.route('/registrar_index', methods=['GET', 'POST'])
def registrar_index():
    dao = RegistrarDao()

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor_id = request.form.get('autor_id')
        descripcion = request.form.get('descripcion')
        isbn = request.form.get('isbn')
        precio = request.form.get('precio', type=float)
        stock = request.form.get('stock', type=int)
        paginas = request.form.get('paginas', type=int)
        categoria_id = request.form.get('categoria_id')
        editorial_id = request.form.get('editorial_id')
        imagen_file = request.files.get('imagen')

        if not titulo or not autor_id or not paginas or not categoria_id or not editorial_id:
            flash('Por favor complete todos los campos obligatorios', 'danger')
            return redirect(url_for('registrar.registrar_index'))

        imagen_bytes = None
        if imagen_file and imagen_file.filename != '':
            imagen_bytes = imagen_file.read()

        try:
            dao.insertar_libro(
                titulo=titulo,
                autor_id=int(autor_id),
                descripcion=descripcion,
                isbn=isbn,
                precio=precio or 0.0,
                stock=stock or 0,
                paginas=paginas,
                categoria_id=int(categoria_id),
                editorial_id=int(editorial_id),
                imagen=imagen_bytes
            )
            flash('Libro registrado correctamente', 'success')
        except Exception as e:
            flash(f'Error al registrar libro: {e}', 'danger')
        
        return redirect(url_for('registrar.registrar_index'))

    libros = dao.get_todos()
    for libro in libros:
        libro['imagen_url'] = url_for('registrar.obtener_imagen', libro_id=libro['id'])

    autores = dao.get_autores()
    categorias = dao.get_categorias()
    editoriales = dao.get_editoriales()

    return render_template(
        'registrar-index.html',
        libros=libros,
        autores=autores,
        categorias=categorias,
        editoriales=editoriales
    )

@registrar.route('/imagen/<int:libro_id>')
def obtener_imagen(libro_id):
    dao = RegistrarDao()
    resultado = dao.obtener_imagen(libro_id)
    if not resultado or not resultado[1]:
        abort(404)
    return Response(resultado[1], mimetype='image/jpeg')
