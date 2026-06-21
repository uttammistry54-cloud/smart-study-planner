import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
instance_path = os.path.join(basedir, "instance")
os.makedirs(instance_path, exist_ok=True)


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(instance_path, 'study_planner.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
