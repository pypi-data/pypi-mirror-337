from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Sequence, Set
from enum import StrEnum

from logicblocks.event.store.conditions import NoCondition, WriteCondition
from logicblocks.event.store.constraints import QueryConstraint
from logicblocks.event.types import (
    CategoryIdentifier,
    LogIdentifier,
    NewEvent,
    StoredEvent,
    StreamIdentifier,
)

# type Listable = identifier.Categories | identifier.Streams
# type Readable = identifier.Log | identifier.Category | identifier.Stream
type Saveable = StreamIdentifier
type Scannable = LogIdentifier | CategoryIdentifier | StreamIdentifier
type Latestable = LogIdentifier | CategoryIdentifier | StreamIdentifier


class EventOrderingGuarantee(StrEnum):
    LOG = "log"


class EventStorageAdapter(ABC):
    @abstractmethod
    async def save(
        self,
        *,
        target: Saveable,
        events: Sequence[NewEvent],
        condition: WriteCondition = NoCondition,
    ) -> Sequence[StoredEvent]:
        raise NotImplementedError()

    @abstractmethod
    async def latest(self, *, target: Latestable) -> StoredEvent | None:
        raise NotImplementedError()

    @abstractmethod
    def scan(
        self,
        *,
        target: Scannable = LogIdentifier(),
        constraints: Set[QueryConstraint] = frozenset(),
    ) -> AsyncIterator[StoredEvent]:
        raise NotImplementedError()
