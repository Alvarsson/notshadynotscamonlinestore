from flask import Flask, Blueprint
from flask_mysqldb import MySQL
from config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = MySQL()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.login import login_bp
    app.register_blueprint(login_bp)

    return app
