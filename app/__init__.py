from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Configuración básica
app.secret_key = b'_5#y2L"F6Q7z\n\xec]/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Inicializar CSRF
csrf = CSRFProtect(app)

# --------- IMPORTAR Y REGISTRAR BLUEPRINTS ---------

# Seguridad (login)
from app.rutas.seguridad.login_routes import logmod
app.register_blueprint(logmod)

# Referenciales (rutas web)
from app.rutas.referenciales.romance.romance_routes import rommod
from app.rutas.referenciales.infantil.infantil_routes import infmod
from app.rutas.referenciales.novedad.novedad_routes import novmod
from app.rutas.referenciales.autor.autor_routes import autormod
from app.rutas.referenciales.editorial.editorial_routes import editorialmod 
from app.rutas.referenciales.tomo.tomo_routes import tomomod
from app.rutas.referenciales.categoria.categoria_routes import categoriamod
from app.rutas.referenciales.medida.medida_routes import medidamod
from app.rutas.referenciales.idioma.idioma_routes import idiomamod

# Contactos
from app.rutas.contactos.contacto_routes import contactomod

# Registrar blueprints con url_prefix para referenciales
modulo0 = '/referenciales'
app.register_blueprint(infmod, url_prefix=f'{modulo0}/infantil')
app.register_blueprint(novmod, url_prefix=f'{modulo0}/novedad')
app.register_blueprint(rommod, url_prefix=f'{modulo0}/romance')
app.register_blueprint(autormod, url_prefix=f'{modulo0}/autor')
app.register_blueprint(editorialmod, url_prefix=f'{modulo0}/editorial')  
app.register_blueprint(tomomod, url_prefix='/referenciales/tomo')
app.register_blueprint(categoriamod, url_prefix='/referenciales/categoria')
app.register_blueprint(medidamod, url_prefix='/referenciales/medida')
app.register_blueprint(idiomamod, url_prefix='/referenciales/idioma')


app.register_blueprint(contactomod, url_prefix='/contacto')



from app.rutas.referenciales.romance.romance_api import romanceapi
from app.rutas.referenciales.infantil.infantil_api import infantilapi
from app.rutas.referenciales.novedad.novedad_api import novedadapi
from app.rutas.referenciales.registrar.registrar_api import registrarapi
from app.rutas.referenciales.autor.autor_api import autorapi
from app.rutas.referenciales.editorial.editorial_api import editorialapi  
from app.rutas.contactos.contacto_api import contactoapi
from app.rutas.referenciales.tomo.tomo_api import tomoapi
from app.rutas.referenciales.categoria.categoria_api import categoriaapi
from app.rutas.referenciales.medida.medida_api import medidaapi
from app.rutas.referenciales.idioma.idioma_api import idiomaapi

api_v1_prefix = '/api/v1'
app.register_blueprint(infantilapi, url_prefix=api_v1_prefix)
app.register_blueprint(romanceapi, url_prefix=api_v1_prefix)
app.register_blueprint(novedadapi, url_prefix=api_v1_prefix)
app.register_blueprint(registrarapi, url_prefix=api_v1_prefix)
app.register_blueprint(contactoapi, url_prefix=api_v1_prefix)
app.register_blueprint(autorapi, url_prefix=api_v1_prefix)
app.register_blueprint(editorialapi, url_prefix=api_v1_prefix) 
app.register_blueprint(tomoapi, url_prefix=api_v1_prefix) 
app.register_blueprint(categoriaapi, url_prefix=api_v1_prefix)
app.register_blueprint(medidaapi, url_prefix=api_v1_prefix)
app.register_blueprint(idiomaapi, url_prefix=api_v1_prefix)

# Registrar blueprint adicional con url_prefix
from app.rutas.referenciales.registrar.registrar_routes import registrar
app.register_blueprint(registrar, url_prefix='/referenciales/registrar')
