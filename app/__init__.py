import os
from flask import Flask
from .config.config import config
from .models.database import init_app as init_db_app

def create_app(config_name=None):
    """Application factory function"""
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_db_app(app)
    
    # Register blueprints
    from .routes.main import main
    from .routes.products import products
    from .routes.payments import payments
    
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(payments)
    
    # Initialize database tables
    with app.app_context():
        from .models.database import init_db
        init_db()
    
    return app 