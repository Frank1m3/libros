from flask import Blueprint, render_template

autormod = Blueprint('autor', __name__, template_folder='templates')

@autormod.route('/autor-index')
def autorIndex():
    return render_template('autor-index.html')
