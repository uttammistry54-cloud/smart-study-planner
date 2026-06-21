from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    with app.app_context():
        from app import models  # noqa: F401  (ensures models are registered)

        from app.auth.routes import auth_bp
        from app.dashboard.routes import dashboard_bp
        from app.tasks.routes import tasks_bp
        from app.planner.routes import planner_bp
        from app.analytics.routes import analytics_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(tasks_bp)
        app.register_blueprint(planner_bp)
        app.register_blueprint(analytics_bp)

        db.create_all()

        from flask import redirect, url_for

        @app.route("/")
        def index():
            return redirect(url_for("dashboard.home"))

    return app
