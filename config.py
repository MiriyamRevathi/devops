import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

class Config:
    """Base application configuration for DevOpsFlow enterprise platform."""
    SECRET_KEY = os.environ.get("DEVOPSFLOW_SECRET_KEY") or secrets.token_hex(32)
    DATA_DIRECTORY = str(DATA_DIR)
    
    # Session & Cookie Config
    SESSION_COOKIE_NAME = "devopsflow_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # Local Persistence Directories
    PROJECTS_DATA_DIR = str(DATA_DIR / "projects")
    REPOSITORIES_DATA_DIR = str(DATA_DIR / "repositories")
    PIPELINES_DATA_DIR = str(DATA_DIR / "pipelines")
    BUILDS_DATA_DIR = str(DATA_DIR / "builds")
    DEPLOYMENTS_DATA_DIR = str(DATA_DIR / "deployments")
    ENVIRONMENTS_DATA_DIR = str(DATA_DIR / "environments")
    SERVICES_DATA_DIR = str(DATA_DIR / "services")
    CONTAINERS_DATA_DIR = str(DATA_DIR / "containers")
    INFRASTRUCTURE_DATA_DIR = str(DATA_DIR / "infrastructure")
    MONITORING_DATA_DIR = str(DATA_DIR / "monitoring")
    LOGS_DATA_DIR = str(DATA_DIR / "logs")
    INCIDENTS_DATA_DIR = str(DATA_DIR / "incidents")
    ALERTS_DATA_DIR = str(DATA_DIR / "alerts")
    SECURITY_DATA_DIR = str(DATA_DIR / "security")
    ARTIFACTS_DATA_DIR = str(DATA_DIR / "artifacts")
    TEAMS_DATA_DIR = str(DATA_DIR / "teams")
    TASKS_DATA_DIR = str(DATA_DIR / "tasks")
    CHANGES_DATA_DIR = str(DATA_DIR / "changes")
    AUDIT_DATA_DIR = str(DATA_DIR / "audit")
    USERS_DATA_DIR = str(DATA_DIR / "users")
    RELEASES_DATA_DIR = str(DATA_DIR / "releases")

    # DORA Metrics Benchmarks (Elite, High, Medium, Low)
    DORA_BENCHMARKS = {
        "deployment_frequency": {
            "elite": "Multiple per day",
            "high": "Between once per day and once per week",
            "medium": "Between once per week and once per month",
            "low": "Fewer than once per month"
        },
        "lead_time": {
            "elite": "< 1 hour",
            "high": "1 day - 1 week",
            "medium": "1 week - 1 month",
            "low": "> 1 month"
        },
        "change_failure_rate": {
            "elite": "0% - 15%",
            "high": "16% - 30%",
            "medium": "31% - 45%",
            "low": "> 45%"
        },
        "mean_time_to_recovery": {
            "elite": "< 1 hour",
            "high": "< 1 day",
            "medium": "1 day - 1 week",
            "low": "> 1 week"
        }
    }

    # Platform Roles & Permissions
    ROLES = {
        "Admin": [
            "read", "write", "delete", "execute_pipelines", "deploy",
            "manage_users", "manage_teams", "approve_changes", "manage_infrastructure"
        ],
        "DevOps Engineer": [
            "read", "write", "execute_pipelines", "deploy",
            "manage_teams", "approve_changes", "manage_infrastructure"
        ],
        "Developer": [
            "read", "write", "execute_pipelines", "create_pr", "create_change"
        ],
        "QA Engineer": [
            "read", "write", "execute_pipelines", "trigger_tests", "create_incident"
        ],
        "Viewer": [
            "read"
        ]
    }

    # Default Target Environments
    ENVIRONMENTS = ["Development", "Testing", "Staging", "Production"]
    
    # Simulation Parameters
    METRICS_COLLECTION_INTERVAL_SECONDS = 10
    MAX_LOG_ENTRIES = 10000
    MAX_AUDIT_ENTRIES = 5000

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    DATA_DIRECTORY = str(DATA_DIR / "test_data")

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
