from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


Handler = Callable[[Any], None]


class MessageBus:
    """Small synchronous message bus used to decouple the demo agents."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, message: Any) -> None:
        for handler in self._subscribers[topic]:
            handler(message)
