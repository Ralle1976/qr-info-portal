from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize database
    from app.database import init_database
    with app.app_context():
        init_database()
    
    # Generate QR codes on startup
    from app.services.qr import QRService
    site_url = os.getenv('SITE_URL', 'http://localhost:5000')
    QRService.save_qr_files(site_url)
    
    # Setup i18n
    from app.services.i18n import t, I18nService
    app.jinja_env.globals.update(t=t)
    app.jinja_env.globals.update(get_current_language=I18nService.get_current_language)
    app.jinja_env.globals.update(SUPPORTED_LANGUAGES=I18nService.SUPPORTED_LANGUAGES)
    
    # Register blueprints
    from app.routes_public import public_bp
    app.register_blueprint(public_bp)
    
    return app