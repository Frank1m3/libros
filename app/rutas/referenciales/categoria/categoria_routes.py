from flask import Blueprint, render_template

categoriamod = Blueprint('categoria', __name__, template_folder='templates')

@categoriamod.route('/categoria-index')
def categoriaIndex():
    return render_template('categoria-index.html')
