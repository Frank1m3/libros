from flask import Blueprint, render_template
from app.dao.referenciales.romance.RomanceDao import RomanceDao

rommod = Blueprint('romance', __name__, template_folder='templates')

@rommod.route('/romance-index')
def romanceIndex():
    dao = RomanceDao()
    libros = dao.getTodos()  # Método que devuelve todos los libros de romance
    return render_template('romance-index.html', libros=libros)

@rommod.route('/romance-detalle/<int:id_libro>')
def romanceDetalle(id_libro):
    dao = RomanceDao()
    libro = dao.get_por_id(id_libro)  # Método que devuelve un libro por ID
    if libro:
        return render_template('romance-detalle.html', libro=libro)
    else:
        return render_template('romance-no_encontrado.html'), 404