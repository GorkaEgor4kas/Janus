"""
Basic Event Bus class, implementation
"""

from collections import defaultdict
from collections.abc import Callable

from janus.event_bus.events import Event, EventType


EventHandler = Callable[[Event], None]


class EventBus:
    def __init__(self):
        self._subscribers: dict[EventType, list[EventHandler]] = defaultdict(list)

    def subscribe(
            self,
            event_type: EventType,
            handler: EventHandler
    ) -> None:
        """Subscribe a handler to a specific event type."""
        handlers = self._subscribers[event_type]
        if handler not in handlers:
            handlers.append(handler)

    def publish(self, event: Event) -> None:
        """Publish an event to all matching subscribers."""
        for handler in self._subscribers.get(event.event_type, []):
            handler(event)