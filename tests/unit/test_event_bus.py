from datetime import datetime, timezone
from uuid import uuid4

from janus.event_bus.event_bus import EventBus
from janus.event_bus.events import Event, EventType


def make_event(event_type: EventType) -> Event:
    "Create a test event"
    return Event(
        event_id=str(uuid4()),
        session_id="test-session",
        timestamp=datetime.now(timezone.utc),
        source="test",
        event_type=event_type,
        payload={}
    )

def test_subscriber_receives_event():
    bus = EventBus()
    received = []
    event_type = next(iter(EventType))
    event = make_event(event_type)

    bus.subscribe(event_type, received.append)
    bus.publish(event=event)

    assert received == [event]


def test_subscriber_receives_only_matching_event_type():
    bus = EventBus()
    received = []

    event_types = list(EventType)
    assert len(event_types) >= 2, "This test requires at least two event types"

    subscribed_type = event_types[0]
    other_type = event_types[1]

    bus.subscribe(subscribed_type, received.append)
    bus.publish(make_event(other_type))

    assert received == []


def test_multiple_subscribers_receive_event():
    bus = EventBus()
    received_a = []
    received_b = []
    event_type = next(iter(EventType))
    event = make_event(event_type)

    bus.subscribe(event_type, received_a.append)
    bus.subscribe(event_type, received_b.append)
    bus.publish(event)

    assert received_a == [event]
    assert received_b == [event]


def test_publish_without_subscribers_does_not_raise():
    bus = EventBus()
    event_type = next(iter(EventType))
    event = make_event(event_type)

    bus.publish(event)


def test_duplicate_subscription_does_not_duplicate_delivery():
    bus = EventBus()
    received = []
    event_type = next(iter(EventType))
    event = make_event(event_type)

    bus.subscribe(event_type, received.append)
    bus.subscribe(event_type, received.append)
    bus.publish(event)

    assert received == [event]


    

