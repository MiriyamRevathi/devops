import hashlib
import hmac
import re
import secrets
from typing import List, Dict, Any, Optional

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
        # Remove script tags and potentially unsafe HTML
        cleaned = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)
        return cleaned.strip()

    @staticmethod
    def check_permission(user_role: str, action: str, role_matrix: Dict[str, List[str]]) -> bool:
        allowed_actions = role_matrix.get(user_role, [])
        return action in allowed_actions or "admin" in user_role.lower()
