from app import app
from flask import Flask, render_template
@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

@app.route('/tienda')
def tienda():
    return render_template('tienda.html')



if __name__ == "__main__":
    app.run(debug=True)