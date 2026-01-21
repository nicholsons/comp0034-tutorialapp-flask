"""Configuration module for the Paralympics application.

Provides a base :class: `Config` and environment-specific subclasses
for production, development, and testing.
"""


class Config:
    """Base configuration.

    Attributes:
        DEBUG (bool): Toggle debug mode. Defaults to ``False``.
        TESTING (bool): Toggle testing mode. Defaults to ``False``.
        CSRF_ENABLED (bool): Enable CSRF protection. Defaults to ``True``.
        SECRET_KEY (str): Secret key for sessions and CSRF. Defaults to ``'dev'``.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dev'


class ProductionConfig(Config):
    """Production configuration.

    Inherits from :class:`Config`. Debugging is disabled in production.
    """
    DEBUG = False


class DevConfig(Config):
    """Development configuration.

    Enables development settings.

    Attributes:
        DEVELOPMENT (bool): Enable development mode. Defaults to ``True``.
        DEBUG (bool): Enable debug mode. Defaults to ``True``.
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration.

    Enables testing mode for the application.

    Attributes:
        TESTING (bool): Toggle testing mode. Defaults to ``True``.
    """
    TESTING = True
