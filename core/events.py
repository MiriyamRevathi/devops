from typing import Dict, List, Callable, Any
import logging

logger = logging.getLogger(__name__)

class EventBus:
    """Local event bus for handling system-wide notifications and audit triggers."""

    _listeners: Dict[str, List[Callable[..., Any]]] = {}

    @classmethod
    def subscribe(cls, event_type: str, callback: Callable[..., Any]) -> None:
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        cls._listeners[event_type].append(callback)

    @classmethod
    def publish(cls, event_type: str, **kwargs: Any) -> None:
        if event_type in cls._listeners:
            for callback in cls._listeners[event_type]:
                try:
                    callback(**kwargs)
                except Exception as e:
                    logger.error(f"Error executing listener for event {event_type}: {e}")

    @classmethod
    def clear(cls) -> None:
        cls._listeners.clear()
