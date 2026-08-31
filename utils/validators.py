import re
from typing import Tuple, Optional

class DataValidator:
    """Comprehensive data validation helper for form and payload processing."""

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip())) if email else False

    @staticmethod
    def validate_project_name(name: str) -> Tuple[bool, Optional[str]]:
        if not name or len(name.strip()) < 3:
            return False, "Project name must be at least 3 characters long."
        if len(name.strip()) > 100:
            return False, "Project name must not exceed 100 characters."
        if not re.match(r'^[a-zA-Z0-9_\-\s]+$', name):
            return False, "Project name can only contain letters, numbers, spaces, hyphens, and underscores."
        return True, None

    @staticmethod
    def validate_version_tag(version: str) -> bool:
        pattern = r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$'
        return bool(re.match(pattern, version.strip()))

    @staticmethod
    def validate_slug(slug: str) -> bool:
        pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
        return bool(re.match(pattern, slug.strip()))
