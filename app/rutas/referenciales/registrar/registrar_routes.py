from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from app.dao.referenciales.registrar.RegistrarDao import RegistrarDao

registrar = Blueprint('registrar', __name__, template_folder='templates')

@registrar.route('/registrar_index', methods=['GET', 'POST'])
def registrar_index():
    dao = RegistrarDao()

    if request.method == 'POST':
        # Captura los datos del formulario
        titulo = request.form.get('titulo')
        autor_id = request.form.get('autor_id')
        descripcion = request.form.get('descripcion')
        isbn = request.form.get('isbn')
        precio = request.form.get('precio', type=float)
        stock = request.form.get('stock', type=int)
        paginas = request.form.get('paginas', type=int)
        categoria_id = request.form.get('categoria_id')
        editorial_id = request.form.get('editorial_id')
        idioma_id = request.form.get('idioma_id')
        medida_id = request.form.get('medida_id')
        edicion_id = request.form.get('edicion_id')
        tomo_id = request.form.get('tomo_id')
        imagen_file = request.files.get('imagen')

        # Validación básica de campos obligatorios
        if not (titulo and autor_id and paginas and categoria_id and editorial_id and idioma_id):
            flash('Por favor, complete todos los campos obligatorios.', 'danger')
            return redirect(url_for('registrar.registrar_index'))

        # Procesar la imagen si se cargó
        imagen_bytes = None
        if imagen_file and imagen_file.filename != '':
            imagen_bytes = imagen_file.read()

        try:
            # Insertar libro en la base de datos
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
                idioma_id=int(idioma_id),
                medida_id=int(medida_id),
                edicion_id=int(edicion_id),
                tomo_id=int(tomo_id),
                imagen=imagen_bytes
            )
            flash('Libro registrado correctamente.', 'success')
        except Exception as e:
            flash(f'Error al registrar libro: {e}', 'danger')
        
        return redirect(url_for('registrar.registrar_index'))

    # GET: Obtener datos para renderizar el formulario y listado
    libros = dao.get_todos()
    for libro in libros:
        libro['imagen_url'] = url_for('registrar.obtener_imagen', libro_id=libro['id'])

    return render_template(
        'registrar_index.html',
        libros=libros,
        autores=dao.get_autores(),
        categorias=dao.get_categorias(),
        editoriales=dao.get_editoriales(),
        idiomas=dao.get_idiomas(),
        medidas=dao.get_medidas(),
        ediciones=dao.get_ediciones(),
        tomos=dao.get_tomos()
    )


@registrar.route('/imagen/<int:libro_id>')
def obtener_imagen(libro_id):
    dao = RegistrarDao()
    imagen = dao.obtener_imagen(libro_id)
    if not imagen:
        abort(404)
    return Response(imagen, mimetype='image/jpeg')
