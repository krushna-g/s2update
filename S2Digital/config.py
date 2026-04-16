import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # simple admin key for the lightweight admin view (override via env)
    ADMIN_KEY = os.environ.get("ADMIN_KEY", "changeme")
    # Centralized contact and social links (override via env in production)
    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "contact@S2Digital.com")
    SOCIAL_FACEBOOK = os.environ.get("SOCIAL_FACEBOOK", "#")
    SOCIAL_INSTAGRAM = os.environ.get("SOCIAL_INSTAGRAM", "#")
    SOCIAL_LINKEDIN = os.environ.get("SOCIAL_LINKEDIN", "#")
    SOCIAL_TWITTER = os.environ.get("SOCIAL_TWITTER", "#")

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, '..', 'S2Digital_dev.db')}"
    )
    DEBUG = True

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, '..', 'S2Digital.db')}"
    )
    DEBUG = False