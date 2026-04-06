# Python Module Organization

## types.py Files

Place all Pydantic models and enums in `types.py` files within each module.

### What Goes in types.py

- Pydantic models (data transfer objects, API schemas, configuration objects)
- Enums used across multiple files in the module
- Type aliases and TypedDict definitions
- Module-level constants closely related to the types

### What Stays Elsewhere

- Django models -> `models.py`
- Django model field choices (`TextChoices`) -> `models.py`, alongside the model
- API endpoint schemas used only in one router -> can stay in `api.py`
- Internal helper types used only in one file -> can stay in that file

## Example

```python
# myapp/types.py
from enum import StrEnum, auto
from pydantic import BaseModel, ConfigDict

class PlanId(StrEnum):
    ESSENTIALS = auto()
    PREMIUM = auto()

class PricingPeriod(StrEnum):
    MONTHLY = auto()
    ANNUAL = auto()

class Plan(BaseModel):
    model_config = ConfigDict(frozen=True)

    plan_id: PlanId
    name: str
    description: str
```

```python
# myapp/models.py — TextChoices stay here
from django.db import models
from django_enum import EnumField

class RefreshStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    STARTED = "STARTED", "Started"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"

class RefreshOperation(models.Model):
    status = EnumField(RefreshStatus, max_length=20)
```

## const.py Files

Place top-level constants in `const.py`. This file should have zero internal imports —
it must not depend on anything else in the module (no models, no types, no services).
This makes it safe to import from anywhere without circular dependency risk.

### What Goes in const.py

- Magic numbers and thresholds (e.g., `MAX_RETRIES = 3`, `DEFAULT_PAGE_SIZE = 25`)
- Configuration defaults (e.g., `DEFAULT_TIMEOUT_SECONDS = 30`)
- String constants used across multiple files (e.g., `CACHE_KEY_PREFIX = "myapp"`)

### What Stays Elsewhere

- Constants closely tied to a type definition -> `types.py`, next to the type
- Django field choices -> `models.py`, as `TextChoices`
- Constants used only in one file -> keep them in that file

```python
# myapp/const.py — no internal imports
MAX_RETRY_ATTEMPTS = 3
DEFAULT_PAGE_SIZE = 25
DEFAULT_TIMEOUT_SECONDS = 30
CACHE_KEY_PREFIX = "myapp"
```

## Typical Module Structure

```
myapp/
├── __init__.py
├── const.py             # Top-level constants (no internal imports)
├── types.py             # Pydantic models, enums, type aliases
├── models.py            # Django models and TextChoices
├── services.py          # Business logic
├── api.py               # API endpoints
├── tasks.py             # Celery tasks
└── tests/
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Pydantic models in services.py | Hard to find, circular import risk | Move to types.py |
| Enums in api.py | Can't reuse in services or tasks | Move to types.py |
| All types in one global file | Too large, hard to navigate | Per-module types.py |
| Constants in const.py that import from models/services | Creates circular deps | const.py must have zero internal imports |
