# Python Data Structure Standards

## Use Pydantic Models for Structured Data

Reach for a Pydantic model ahead of every other way of holding structured data:
dataclasses, dicts, `TypedDict`s, tuples, and named tuples. Make it frozen whenever
nothing needs to mutate it, which is most of the time:

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

Leave `extra` at its default. A model often outlives the schema it was written under — a
stored JSON snapshot, a cached payload, a response persisted months ago — so `"forbid"`
turns a key nobody reads into a failed load of older data.

### Enable the mypy plugin

A project using Pydantic enables its mypy plugin. Set `init_forbid_extra` so a misspelled
keyword in a constructor call is caught at the call site rather than silently ignored at
runtime, and `init_typed` so argument types are checked there too.

```toml
# pyproject.toml
[tool.mypy]
plugins = ["pydantic.mypy"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
```

### Define a shared base

Put the shared `model_config` on one base class in the project's utility module and
subclass it, rather than repeating `ConfigDict(...)` in every model.

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
