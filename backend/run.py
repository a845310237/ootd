"""Flask application entry point for OOTD backend."""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.config import get_config
from app.models import database

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app.

    Args:
        config_name: Configuration name (development/production/testing)

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import models to ensure they're registered with SQLAlchemy
    from app.models.user import User
    from app.models.clothing import Clothing
    from app.models.outfit import Outfit
    from app.models.outfit_item import OutfitItem

    # Register API blueprints
    from app.api.auth import auth_bp
    from app.api.user import user_bp
    from app.api.wardrobe import wardrobe_bp
    from app.api.outfits import outfits_bp
    from app.api.upload import upload_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(wardrobe_bp, url_prefix='/api/wardrobe')
    app.register_blueprint(outfits_bp, url_prefix='/api/outfits')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'app_name': config.APP_NAME,
            'debug': config.DEBUG
        })

    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint."""
        return jsonify({
            'message': 'OOTD API Server',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'user': '/api/user',
                'wardrobe': '/api/wardrobe',
                'outfits': '/api/outfits',
                'upload': '/api/upload'
            }
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({'error': 'Internal server error'}), 500

    # Initialize database
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=9003,
        debug=get_config().DEBUG
    )
