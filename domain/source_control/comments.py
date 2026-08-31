from typing import Dict, Any, Optional
from utils.helpers import get_utc_now_iso, generate_id

class PullRequestComment:
    def __init__(self, pr_id: str, author: str, content: str, line_number: Optional[int] = None, comment_id: Optional[str] = None):
        self.id = comment_id or generate_id("cmt")
        self.pr_id = pr_id
        self.author = author
        self.content = content
        self.line_number = line_number
        self.created_at = get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "pr_id": self.pr_id, "author": self.author, "content": self.content, "line_number": self.line_number, "created_at": self.created_at}
