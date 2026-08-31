import re
from typing import List, Dict, Any

class SecretPatternScanner:
    PATTERNS = {
        "AWS Access Key": r'AKIA[0-9A-Z]{16}',
        "Generic Secret Token": r'(api_key|secret_key|private_key)\s*=\s*["'][A-Za-z0-9+/=]{16,}["']',
        "RSA Private Key": r'-----BEGIN RSA PRIVATE KEY-----'
    }

    @classmethod
    def scan_content(cls, content: str) -> List[Dict[str, Any]]:
        matches = []
        for name, pattern in cls.PATTERNS.items():
            found = re.findall(pattern, content)
            if found:
                matches.append({"pattern": name, "matches_count": len(found)})
        return matches
