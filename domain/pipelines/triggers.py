from typing import List

class PipelineTriggerCondition:
    def __init__(self, trigger_type: str = "on_push", branches: List[str] = None, paths_ignore: List[str] = None):
        self.trigger_type = trigger_type
        self.branches = branches or ["main", "release/*"]
        self.paths_ignore = paths_ignore or ["docs/*", "README.md"]

    def should_trigger(self, branch: str, changed_files: List[str]) -> bool:
        if not any(b == branch or (b.endswith("*") and branch.startswith(b[:-1])) for b in self.branches):
            return False
        if all(any(f.startswith(ign.rstrip("*")) for ign in self.paths_ignore) for f in changed_files):
            return False
        return True
