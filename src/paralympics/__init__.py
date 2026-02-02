from flask import Flask

from paralympics.config import DevConfig

def create_app(config_class=DevConfig):
    """Create and configure the Flask application.

    This provides the application factory for the Paralympics Flask app.

    The factory pattern is used to create and configure the Flask application
    instance so it can be created with different configurations for testing,
    development, or production.

    Args:
        config_class (type): Configuration class used to configure the app.
                             Defaults to `DevConfig`.

    Returns:
        flask.Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register the blueprint
    from paralympics.main import bp
    app.register_blueprint(bp)

    return app
