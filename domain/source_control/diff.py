from typing import List, Dict

class CommitDiff:
    def __init__(self, commit_hash: str, file_path: str, old_lines: List[str], new_lines: List[str]):
        self.commit_hash = commit_hash
        self.file_path = file_path
        self.old_lines = old_lines
        self.new_lines = new_lines

    def compute_stats(self) -> Dict[str, int]:
        additions = sum(1 for line in self.new_lines if line not in self.old_lines)
        deletions = sum(1 for line in self.old_lines if line not in self.new_lines)
        return {"additions": additions, "deletions": deletions, "total_changes": additions + deletions}
