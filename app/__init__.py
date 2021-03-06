from flask import Flask
from app.common.db import db
from flask_cors import CORS
from app.common.ext import mh, migrate, jwt
from flask_restful import Api
#config app
from app.config.default import config
#app Extension
from app.common.command import command_app
from app.common.jwt_bihavier import jwt_callbacks
from app.common.error_handlers import register_error_handlers
#blueprint modules
from app.usuarios.routes import modulo_usuarios
from app.usuarios.auth.routes import modulo_login

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    #inicializa cors
    CORS(app)
    #Inicializa las extensiones
    db.init_app(app)
    mh.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    #Captura todos los errores 404
    Api(app, catch_all_404s=True)
    #Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False

    
    #Registra los blueprints
    app.register_blueprint(modulo_login)
    app.register_blueprint(modulo_usuarios)

    #Registra los comandos configurados en esta aplicación
    command_app(app)
    #Registra manejadores de errores personalizados
    register_error_handlers(app)
    #Callbacks de control de comportamiento de los jwt
    jwt_callbacks(jwt)
    

    return app



