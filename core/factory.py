import os
from flask import Flask, render_template, session, g
from config import config_by_name, Config
from core.extensions import extensions
from core.security import SecurityManager

def create_app(config_name: str = "default") -> Flask:
    """Flask Application Factory for DevOpsFlow enterprise platform."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    # Load configuration
    cfg = config_by_name.get(config_name, Config)
    app.config.from_object(cfg)

    # Register Extensions
    extensions.app = app

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.projects import projects_bp
    from routes.repositories import repositories_bp
    from routes.pipelines import pipelines_bp
    from routes.deployments import deployments_bp
    from routes.releases import releases_bp
    from routes.environments import environments_bp
    from routes.services import services_bp
    from routes.containers import containers_bp
    from routes.infrastructure import infrastructure_bp
    from routes.monitoring import monitoring_bp
    from routes.logs import logs_bp
    from routes.incidents import incidents_bp
    from routes.alerts import alerts_bp
    from routes.security import security_bp
    from routes.artifacts import artifacts_bp
    from routes.teams import teams_bp
    from routes.tasks import tasks_bp
    from routes.changes import changes_bp
    from routes.audit import audit_bp
    from routes.analytics import analytics_bp
    from routes.users import users_bp
    from routes.testing import testing_bp
    from routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(repositories_bp)
    app.register_blueprint(pipelines_bp)
    app.register_blueprint(deployments_bp)
    app.register_blueprint(releases_bp)
    app.register_blueprint(environments_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(containers_bp)
    app.register_blueprint(infrastructure_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(artifacts_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(changes_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(testing_bp)
    app.register_blueprint(settings_bp)

    # Context Processors & Template Helpers
    @app.context_processor
    def inject_global_context():
        user_role = session.get("role", "Viewer")
        user_perms = SecurityManager.get_user_permissions(user_role)
        allowed_nav = Config.ROLE_NAV.get(user_role, Config.ROLE_NAV["Viewer"])
        
        return {
            "current_user": {
                "id": session.get("user_id"),
                "username": session.get("username", "Guest"),
                "role": user_role,
                "full_name": session.get("full_name", "Guest User")
            },
            "user_permissions": user_perms,
            "has_permission": lambda perm: SecurityManager.has_permission(user_role, perm),
            "allowed_nav": allowed_nav,
            "roles": Config.ROLES
        }

    # Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app
