"""
Basic Event Bus class, implementation
"""

from collections import defaultdict
from collections.abc import Callable

from janus.event_bus.events import Event


Event_handler = Callable[[Event], None]


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Event_handler]] = defaultdict(list)

    def subscribe(
            self,
            event_type: str,
            handler: Event_handler
    ) -> None:
        """Subscribe a handler to a specific event type."""
        # TODO: register the handler
        pass

    def publish(self, event: Event) -> None:
        """Publish an event to all matching subscribers."""
        # TODO: notify subscribers
        pass