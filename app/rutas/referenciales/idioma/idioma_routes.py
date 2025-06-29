from flask import Blueprint, render_template

idiomamod = Blueprint('idioma', __name__, template_folder='templates')

@idiomamod.route('/idioma-index')
def idiomaIndex():
    return render_template('idioma-index.html')
