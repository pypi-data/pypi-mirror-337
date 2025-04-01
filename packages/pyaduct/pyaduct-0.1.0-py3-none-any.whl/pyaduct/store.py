from typing import Protocol
from uuid import UUID

from .models import Message


class IMessageStore(Protocol):
    def add_message(self, message: Message) -> None:
        """Add a message to the store."""
        ...

    def get_message(self, message_id: UUID) -> Message | None:
        """Retrieve a message by its ID."""
        ...

    def delete_message(self, message_id: UUID) -> None:
        """Delete a message from the store."""
        ...

    @property
    def messages(self) -> list[Message]:
        """Return an iterator over the messages in the store."""
        ...


class InmemMessageStore(IMessageStore):
    """In-memory message store implementation."""

    def __init__(self):
        self._messages: list[Message] = []

    def add_message(self, message: Message) -> None:
        self._messages.append(message)

    def get_message(self, message_id: UUID) -> Message | None:
        for message in self._messages:
            if message.id == message_id:
                return message

    def delete_message(self, message_id: UUID) -> None:
        if message_id in self._messages:
            del self._messages[message_id]

    @property
    def messages(self) -> list[Message]:
        return self._messages
