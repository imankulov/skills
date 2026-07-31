# Python Module Organization

## types.py Files

Place a Pydantic model, enum, or type alias in the module's `types.py` once more than one
file in that module uses it. A type used by a single file stays in that file, near the top.

### What Goes in types.py

- Pydantic models (data transfer objects, API schemas, configuration objects)
- Enums
- Type aliases and TypedDict definitions
- Module-level constants closely related to the types

### What Stays Elsewhere

- Django models -> `models.py`
- Django model field choices (`TextChoices`) -> `models.py`, alongside the model
- API endpoint schemas used only in one router -> can stay in `api.py`

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

## Typical Structure

Exceptions and configuration sit at the app level, above every module that uses them. A module
holds its own data layer, services, and entry points — no `exceptions.py` inside it. Modules are
domain-named siblings; each one has the same shape.

```
myapp/
├── __init__.py
├── config.py                # App configuration
├── exceptions.py            # App-wide exception hierarchy
├── authentication/          # Sibling module, same shape
├── annual_reports/          # Sibling module, same shape
└── billing/
    ├── __init__.py
    ├── const.py             # Top-level constants (no internal imports)
    ├── types.py             # Pydantic models, enums, type aliases
    ├── models.py            # Django models and TextChoices
    ├── services.py          # Business logic
    ├── api.py               # API endpoints
    ├── tasks.py             # Celery tasks
    └── tests/
```
