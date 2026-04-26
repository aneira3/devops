from flask import Flask
from flask_restful import Api
from config import Config
from app.models.blacklist import db
from app.schemas.blacklist_schema import ma
from app.auth import jwt, create_static_token
from app.resources.blacklist_resource import BlacklistResource, BlacklistCheckResource

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    
    # Create API
    api = Api(app)
    
    # Add resources
    api.add_resource(BlacklistResource, '/blacklists')
    api.add_resource(BlacklistCheckResource, '/blacklists/<string:email>')
    
    # Avoid opening a production DB connection as a side effect of importing
    # the module; tests inject their own database configuration explicitly.
    if not app.config.get('TESTING') and not app.config.get('SKIP_DB_INIT', False):
        with app.app_context():
            db.create_all()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthyy', 'service': 'blacklist-microservice'}, 200
    
    @app.route('/token', methods=['POST'])
    def get_token():
        token = create_static_token(app)
        return {'access_token': token}, 200
    
    return app

application = create_app({'SKIP_DB_INIT': True})

if __name__ == '__main__':
    application = create_app()
    application.run(debug=True, host='0.0.0.0', port=5000)
