from flask import Blueprint, render_template

novmod = Blueprint('novedad', __name__, template_folder='templates')

@novmod.route('/novedad-index')
def novedadIndex():
    return render_template('novedad-index.html')