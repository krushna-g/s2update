import os
from flask import Flask
from .extensions import db
from .main.routes import bp as main_bp
from .chat.routes import bp as chat_bp
import click

def create_app(config=None):
    pkg_dir = os.path.dirname(__file__)
    app = Flask(
        __name__,
        template_folder=os.path.join(pkg_dir, "templates"),
        static_folder=os.path.join(pkg_dir, "static"),
    )

    # load config (dotted path, dict, class or None)
    if isinstance(config, str):
        app.config.from_object(config)
    elif isinstance(config, dict):
        app.config.update(config)
    elif config is None:
        app.config.from_object("S2Digital.config.DevConfig")
    else:
        app.config.from_object(config)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp, url_prefix="/api")

    # inject site config into all templates to avoid using current_app in templates
    @app.context_processor
    def inject_site_config():
        return {
            "site": {
                "CONTACT_EMAIL": app.config.get("CONTACT_EMAIL"),
                "SOCIAL_FACEBOOK": app.config.get("SOCIAL_FACEBOOK"),
                "SOCIAL_INSTAGRAM": app.config.get("SOCIAL_INSTAGRAM"),
                "SOCIAL_LINKEDIN": app.config.get("SOCIAL_LINKEDIN"),
                "SOCIAL_TWITTER": app.config.get("SOCIAL_TWITTER"),
            }
        }

    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        with app.app_context():
            db.create_all()
        click.echo("Initialized the database.")

    return app