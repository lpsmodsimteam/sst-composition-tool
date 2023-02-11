"""
Driver function for the Flask application. This script implements the Flask
configurations, views and database functionality.
"""

from flask import Flask

from .routes import bp
from .demo import demo_bp


def create_app() -> Flask:
    """
    The Flask application factory function.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = "static"
    app.url_map.strict_slashes = False
    app.config["UPLOAD_FOLDER"] = "db"
    app.register_blueprint(bp)
    app.register_blueprint(demo_bp)

    return app
