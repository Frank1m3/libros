from flask import Blueprint, render_template

tomomod = Blueprint('tomo', __name__, template_folder='templates')

@tomomod.route('/tomo-index')
def tomoIndex():
    return render_template('tomo-index.html')
