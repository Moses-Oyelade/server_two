from flask import Flask
from extensions import db, jwt
from auth import auth_bp
from api import api_bp


def create_app():
    
    app = Flask(__name__)
    
    app.config.from_prefixed_env()
    
    # initialize extentions
    db.init_app(app)
    jwt.init_app(app)
    
    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Routing blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    
    return app