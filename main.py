from flask import Flask, jsonify
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
    app.register_blueprint(api_bp, url_prefix='/api')
    
    
    # jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({"message":"Token has expired", "error":"token_expired"})
    
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed", "error":"invalid_token"})
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"Request does not contain valid token", "error":"authorization_header"})
    
    return app