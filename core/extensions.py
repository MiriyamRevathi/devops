"""Extensions module for Flask application dependencies."""

class LocalExtensions:
    """Registry for local extensions and shared singletons."""
    def __init__(self):
        self.app = None

extensions = LocalExtensions()
