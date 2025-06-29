from flask import Blueprint, render_template

editorialmod = Blueprint('editorial', __name__, template_folder='templates')

@editorialmod.route('/editorial-index')
def editorialIndex():
    return render_template('editorial-index.html')
