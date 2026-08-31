import datetime
import uuid
import random
import string
from typing import Any, Dict, List

def generate_id(prefix: str = "") -> str:
    """Generate a unique formatted string identifier."""
    unique_str = uuid.uuid4().hex[:12]
    return f"{prefix}_{unique_str}" if prefix else unique_str

def get_utc_now_iso() -> str:
    """Return ISO format string of current UTC timestamp."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def format_timestamp(iso_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format ISO timestamp string into human readable representation."""
    if not iso_str:
        return "N/A"
    try:
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime(fmt)
    except Exception:
        return iso_str

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length with ellipsis."""
    if not text or len(text) <= max_length:
        return text or ""
    return text[:max_length] + "..."

def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage safely."""
    if not total or total <= 0:
        return 0.0
    return round((part / total) * 100, 2)
