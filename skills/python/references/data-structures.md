# Python Data Structure Standards

## Use Pydantic Models for Structured Data

Prefer Pydantic models over raw dictionaries. Use frozen models (immutable) by default:

```python
from pydantic import BaseModel, ConfigDict

class UserData(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_id: int
    name: str
    email: str | None = None

# Usage
user = UserData(user_id=1, name="John Doe")
```

## Enums

Use the right enum type for the context:

- **String-valued enums**: `StrEnum` with `auto()`
- **Integer enums**: `IntEnum`
- **Django model field choices**: `models.TextChoices` — see the django skill

```python
from enum import StrEnum, auto

class UserRole(StrEnum):
    ADMIN = auto()
    MODERATOR = auto()
    USER = auto()
```

## Interfaces

Prefer an explicit `abc.ABC` base class with abstract methods, named with an `I` prefix. Avoid
`typing.Protocol` unless structural typing is specifically required — an ABC makes subclasses declare
the interface they implement, so the relationship is visible at the definition site.

```python
from abc import ABC, abstractmethod


class ICacheCodec[T](ABC):
    """Encode and decode one cache payload type."""

    identity: str

    @abstractmethod
    def encode(self, value: T) -> bytes:
        """Encode a value for storage."""

    @abstractmethod
    def decode(self, payload: bytes) -> T:
        """Decode a stored payload."""


class Utf8Codec(ICacheCodec[str]):
    identity = "utf-8"

    def encode(self, value: str) -> bytes:
        return value.encode("utf-8")

    def decode(self, payload: bytes) -> str:
        return payload.decode("utf-8")
```

Use `TypedDict` only when interfacing with external libraries that require dict types;
prefer Pydantic models everywhere else, over raw dictionaries and tuples alike.
