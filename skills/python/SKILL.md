---
name: python
description: |
  Opinionated Python coding standards for clean, type-safe code. Use when writing
  or reviewing Python functions, classes, type hints, data structures, enums, or
  module organization. Applies to any Python 3.12+ project.
  Also use when deciding on app architecture, where to place business logic, how
  to organize modules, or choosing between dicts vs Pydantic models.
  Do NOT use for: Django-specific patterns (use django skill), test files (use pytest
  skill), frontend code, or shell scripts.
---

# Python Coding Standards

Opinionated conventions for modern Python (3.12+) emphasizing type safety, clear
function signatures, consistent module organization, and a layered architecture.

## App Architecture

Dependencies flow downward. Higher-level modules import from lower-level modules,
never the reverse.

```
+-------------------------------------------------------+
|  api.py, tasks.py, admin.py, ...  (entry points)      |
+----------------------------+---------------------------+
                             | imports
                             v
+-------------------------------------------------------+
|              services.py  (business logic)             |
+----------------------------+---------------------------+
                             | imports
                             v
+-------------------------------------------------------+
|      models.py, types.py, const.py  (data layer)      |
+-------------------------------------------------------+
```

**Entry points** (api.py, tasks.py, admin.py, cli.py, etc.) are thin wrappers that
call service functions. They handle request parsing, scheduling, and output formatting
but contain no business logic.

**services.py** holds all business logic. Service functions are reusable across any
entry point — an API endpoint, a background task, a CLI command, and an admin action
can all call the same service function.

**Data layer** (models.py, types.py, const.py) defines data structures with zero
business logic. `const.py` must have no internal imports — it's safe to import from
anywhere.

All imports should be at the top of the module file. Deferred imports inside functions
are acceptable only to break circular dependencies — and if you need them frequently,
the module structure needs refactoring.

| Avoid | Why | Instead |
|-------|-----|---------|
| Business logic in entry points | Can't reuse across API/CLI/tasks | Move to services.py |
| Entry points importing each other | Circular deps, tight coupling | Both import from services |
| Deferred imports without justification | Hides dependency problems | Top-level imports, fix module structure |

### Entry Point Naming Convention

Service functions own the base name. Entry points that wrap them add a suffix for their
layer:

| Layer | Suffix | Example |
|-------|--------|---------|
| Service (business logic) | *(none)* | `create_user()` |
| API endpoint | `_api` | `create_user_api()` |
| CLI command | `_cli` | `create_user_cli()` |
| Background task | `_task` | `create_user_task()` |

This keeps imports clean — `from myapp.services import create_user` works in every
entry point without aliasing. Never use `import ... as` to work around naming
conflicts; use the suffix instead.

All entry points call the same service function:

```python
# services.py
def create_user(*, email: str, name: str) -> User:
    ...

# api.py
def create_user_api(request: AuthenticatedHttpRequest, input_data: CreateUserInput) -> UserResponse:
    user = create_user(email=input_data.email, name=input_data.name)
    return UserResponse.from_model(user)

# tasks.py
def create_user_task(email: str, name: str) -> None:
    create_user(email=email, name=name)

# cli.py
def create_user_cli(email: str, name: str) -> None:
    user = create_user(email=email, name=name)
    click.echo(f"Created {user.email}")
```

## Functions

- Type-annotate all parameters and return values
- Google-style docstrings without type information (types are in the signature)
- For functions with more than 3 parameters, use keyword-only arguments (`*`)
- Prefix internal helper functions with underscore
- Keep helper function documentation concise

```python
def process_user_data(*, user_id: int, name: str, email: str, age: int) -> dict[str, any]:
    """Process and validate user data.

    Args:
        user_id: Unique identifier for the user
        name: User's full name
        email: User's email address
        age: User's age in years

    Returns:
        Processed user data dictionary with validation status
    """
    return {"status": "valid", "data": {"id": user_id, "name": name}}

def calculate_total(price: float, quantity: int) -> float:
    """Calculate total cost for an item."""
    return price * quantity

def _format_name(first: str, last: str) -> str:
    """Combines first and last name into full name."""
    return f"{first} {last}".strip()
```

| Avoid | Why | Instead |
|-------|-----|---------|
| Missing type hints | No IDE support, no static checking | Annotate everything |
| Types in docstrings | Redundant with annotations, drifts | Google-style without types |
| Positional args for 4+ params | Call sites are unreadable | `*` to force keyword args |
| Verbose helper docstrings | Noise for simple functions | One-line docstring |

## Type Hints (PEP 604)

Use modern union syntax. Never import from `typing` for basic types:

```python
# Good
def process(items: list[str], config: dict[str, int] | None = None) -> bool | None:
    return True

# Bad — deprecated syntax
from typing import List, Dict, Optional, Union
def process(items: List[str], config: Optional[Dict[str, int]] = None) -> Union[bool, None]:
    return True
```

## Class Naming

Treat abbreviations as single words in CamelCase class names. Capitalize only the
first letter:

| Correct | Wrong |
|---------|-------|
| `JsonParser` | `JSONParser` |
| `ApiClient` | `APIClient` |
| `DbConnection` | `DBConnection` |
| `HttpResponse` | `HTTPResponse` |
| `SqlQuery` | `SQLQuery` |

## References

For detailed patterns on specific topics, load these as needed:

- [Data structures](references/data-structures.md) — Pydantic vs dicts, enums, TypedDict
- [Module organization](references/module-organization.md) — types.py, const.py placement rules
- [URL parsing](references/url-parsing.md) — furl for all URL manipulation

## Verification

After writing Python code, verify:

- [ ] Business logic lives in services.py, not in entry points
- [ ] Entry points are thin wrappers calling service functions
- [ ] All imports are at the top of the file
- [ ] All function parameters and returns have type annotations
- [ ] Functions with 4+ parameters use keyword-only arguments
- [ ] No `typing.Union`, `typing.Optional`, `typing.List`, `typing.Dict` imports
- [ ] Class abbreviations use CamelCase (JsonParser, not JSONParser)
- [ ] Helper functions are prefixed with underscore
