import hashlib
import hmac
import re
import secrets
from functools import wraps
from typing import List, Dict, Any, Optional, Callable
from flask import session, redirect, url_for, flash, render_template, request, jsonify
from config import Config

class SecurityManager:
    """Security engine handling password hashing, RBAC permissions, and input sanitization."""

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> str:
        if not salt:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()
        return f"{salt}${pwd_hash}"

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            salt, stored_hash = hashed_password.split("$", 1)
            calculated_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                100000
            ).hex()
            return hmac.compare_digest(stored_hash, calculated_hash)
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def sanitize_input(value: str) -> str:
        if not isinstance(value, str):
            return value
        cleaned = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)
        return cleaned.strip()

    @staticmethod
    def get_user_permissions(user_role: str) -> List[str]:
        return Config.ROLES.get(user_role, [])

    @staticmethod
    def has_permission(user_role: str, permission: str) -> bool:
        allowed_permissions = Config.ROLES.get(user_role, [])
        return permission in allowed_permissions or user_role == "Admin"


def login_required(f: Callable) -> Callable:
    """Decorator requiring an active user session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            if request.is_json or request.path.startswith("/api/"):
                return jsonify({"error": "Unauthorized", "message": "Authentication required."}), 401
            flash("Please sign in to access DevOpsFlow.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission: str) -> Callable:
    """Decorator enforcing granular RBAC permission at backend route level."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({"error": "Unauthorized", "message": "Authentication required."}), 401
                flash("Please sign in to access DevOpsFlow.", "warning")
                return redirect(url_for("auth.login"))

            user_role = session.get("role", "Viewer")
            if not SecurityManager.has_permission(user_role, permission):
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({
                        "error": "Forbidden",
                        "message": f"Access Denied: Role '{user_role}' lacks permission '{permission}'."
                    }), 403
                return render_template(
                    "errors/403.html",
                    required_permission=permission,
                    user_role=user_role
                ), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(*roles: str) -> Callable:
    """Decorator enforcing specific role membership at backend route level."""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({"error": "Unauthorized", "message": "Authentication required."}), 401
                flash("Please sign in to access DevOpsFlow.", "warning")
                return redirect(url_for("auth.login"))

            user_role = session.get("role", "Viewer")
            if user_role not in roles and "Admin" not in roles and user_role != "Admin":
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({
                        "error": "Forbidden",
                        "message": f"Access Denied: Action restricted to roles: {', '.join(roles)}."
                    }), 403
                return render_template(
                    "errors/403.html",
                    required_role=", ".join(roles),
                    user_role=user_role
                ), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
