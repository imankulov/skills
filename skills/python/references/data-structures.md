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

- **Django model field choices**: `models.TextChoices` (provides labels for admin/forms)
- **Other string-valued enums**: `StrEnum` with `auto()`
- **Integer enums**: `IntEnum`

```python
# Django model choices
from django.db import models

class ScheduleReason(models.TextChoices):
    PROPERTY_CREATED = "PROPERTY_CREATED", "Property Created"
    PROPERTY_UPDATED = "PROPERTY_UPDATED", "Property Updated"
    ADMIN_REQUESTED = "ADMIN_REQUESTED", "Admin Requested"

# General-purpose string enum
from enum import StrEnum, auto

class UserRole(StrEnum):
    ADMIN = auto()
    MODERATOR = auto()
    USER = auto()
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Raw dictionaries for structured data | No validation, no IDE support | Pydantic models |
| Tuples for structured data | Positional access is error-prone | Pydantic models |
| String literals for fixed sets | Typos, no completion | Enums |
| Inline choice tuples in Django models | Can't reference values, no methods | TextChoices class |
| TypedDict for internal code | Less validation than Pydantic | Pydantic models |

Use `TypedDict` only when interfacing with external libraries that require dict types.
