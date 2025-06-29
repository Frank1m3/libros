from flask import Blueprint, render_template

medidamod = Blueprint('medida', __name__, template_folder='templates')

@medidamod.route('/medida-index')
def medidaIndex():
    return render_template('medida-index.html')
