import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from app.config import get_config

config_name = os.environ.get('APP_ENV') or 'prod'

app = Flask(__name__)
app.config.from_object(get_config(config_name))
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from app.routes import usuarios_bp

app.register_blueprint(usuarios_bp, url_prefix='/api/users')
