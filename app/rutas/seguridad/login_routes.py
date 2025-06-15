from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from app.dao.referenciales.usuario.login_dao import LoginDao

logmod = Blueprint('login', __name__, template_folder='templates')

@logmod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_nombre = request.form['usuario_nombre']
        usuario_clave = request.form['usuario_clave']
        
        login_dao = LoginDao()
        usuario_encontrado = login_dao.buscarUsuario(usuario_nombre)
        
        if usuario_encontrado and 'usu_nick' in usuario_encontrado:
            password_hash_del_usuario = usuario_encontrado['usu_clave']
            
            if check_password_hash(pwhash=password_hash_del_usuario, password=usuario_clave):
                session.clear()
                session.permanent = True
                session['usu_id'] = usuario_encontrado['usu_id']
                session['usuario_nombre'] = usuario_nombre
                session['nombre_persona'] = usuario_encontrado['nombre_persona']
                session['grupo'] = usuario_encontrado['grupo']
                
                return redirect(url_for('login.inicio'))

            else:
                flash('Contraseña incorrecta', 'warning')
                return redirect(url_for('login.login'))

        else:
            flash('Error de inicio, no existe este usuario', 'danger')
            return redirect(url_for('login.login'))

    return render_template('login.html')


@logmod.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'warning')
    return redirect(url_for('login.login'))


@logmod.route('/')
def inicio():
    if 'usuario_nombre' in session:
        return render_template('base.html')
    else:
        return redirect(url_for('login.login'))


@logmod.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usu_nick = request.form['usuario_nombre']
        usu_clave = request.form['usuario_clave']
        usu_email = request.form['usuario_email']  # Campo del formulario

        login_dao = LoginDao()
        
        if login_dao.existeNick(usu_nick):
            flash("Este usuario ya existe, elegí otro.", "warning")
            return redirect(url_for('login.registro'))
        
        gru_id = 2  # Grupo 'cliente'
        
        # Enviar los datos al DAO, este se encarga de hashear
        nuevo_id = login_dao.crearUsuario(usu_nick, usu_clave, usu_email, gru_id)
        
        if nuevo_id:
            flash("Usuario registrado con éxito. Ahora podés iniciar sesión.", "success")
            return redirect(url_for('login.login'))
        else:
            flash("Ocurrió un error al registrar el usuario", "danger")
            return redirect(url_for('login.registro'))

    return render_template('registro.html')


@logmod.route('/invitado')
def invitado():
    session.clear()
    session['usuario_nombre'] = 'invitado'
    session['grupo'] = 'invitado'
    flash('Ingresaste como invitado', 'info')
    return redirect(url_for('login.inicio'))

