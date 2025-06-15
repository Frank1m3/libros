from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Clave secreta para formularios y sesiones (puede estar en configuración separada)
app.secret_key = b'_5#y2L"F6Q7z\n\xec]/'

# Inicializar CSRF con la app
csrf = CSRFProtect(app)

# Duración de la sesión (15 minutos)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# --------- BLUEPRINTS ---------

# Seguridad (login)
from app.rutas.seguridad.login_routes import logmod
app.register_blueprint(logmod)

# Referenciales
from app.rutas.referenciales.romance.romance_routes import rommod
from app.rutas.referenciales.infantil.infantil_routes import infmod
from app.rutas.referenciales.novedad.novedad_routes import novmod


# Contactos
from app.rutas.contactos.contacto_routes import contactomod

# Registrar blueprints con url_prefix
modulo0 = '/referenciales'
app.register_blueprint(infmod, url_prefix=f'{modulo0}/infantil')
app.register_blueprint(novmod, url_prefix=f'{modulo0}/novedad')
app.register_blueprint(rommod, url_prefix=f'{modulo0}/romance')

# Importante: el url_prefix aquí es '/contacto' (sin 's'), debe coincidir con tus URLs y links
app.register_blueprint(contactomod, url_prefix='/contacto')

# --------- APIS v1 ---------

from app.rutas.referenciales.romance.romance_api import romanceapi
from app.rutas.referenciales.infantil.infantil_api import infantilapi
from app.rutas.referenciales.novedad.novedad_api import novedadapi
from app.rutas.referenciales.registrar.registrar_api import registrarapi
from app.rutas.contactos.contacto_api import contactoapi

apiversion1 = '/api/v1'
app.register_blueprint(infantilapi, url_prefix=apiversion1)
app.register_blueprint(romanceapi, url_prefix=apiversion1)
app.register_blueprint(novedadapi, url_prefix=apiversion1)
app.register_blueprint(registrarapi, url_prefix=apiversion1)
app.register_blueprint(contactoapi, url_prefix=apiversion1)


from app.rutas.referenciales.registrar.registrar_routes import registrar

# Registra el blueprint con url_prefix
app.register_blueprint(registrar, url_prefix='/referenciales/registrar')
