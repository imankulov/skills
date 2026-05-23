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

- Type-annotate parameters and return values when the type carries information
- Don't annotate for the sake of annotating. If the only honest type is `Any` (e.g., a wrapper around an optional/dynamically-imported library, a generic decorator, a `**kwargs` passthrough), leave it unannotated rather than sprinkling `Any` everywhere — `Any` adds noise without giving the reader, the type checker, or the IDE anything useful
- Google-style docstrings without type information (types are in the signature)
- For functions with more than 3 parameters, use keyword-only arguments (`*`)
- Prefix internal helper functions with underscore
- Keep helper function documentation concise
- Order a file top-down like a newspaper — the *newspaper metaphor* from Robert C. Martin's *Clean Code*: public functions (the headline) first, helpers (the supporting detail) below them. A `_helper` used by exactly one public function should sit directly under it. (Pydantic/dataclass types are an exception — group them near the top so they're defined before use.)

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
| Missing type hints where a real type exists | No IDE support, no static checking | Annotate with the actual type |
| `Any` annotations on every param of a passthrough/wrapper | Noise without information | Leave unannotated |
| Types in docstrings | Redundant with annotations, drifts | Google-style without types |
| Positional args for 4+ params | Call sites are unreadable | `*` to force keyword args |
| Verbose helper docstrings | Noise for simple functions | One-line docstring |

## Leading Underscores

A single leading underscore says "internal — don't call or import this from outside this module." Reserve it for two cases where outside use would cause a real problem:

- **Internal functions and methods.** A `_helper` may skip validation the public API enforces, hold an invariant of the surrounding function, or change shape at any time. The underscore protects callers from depending on it.
- **Mutable singleton state used for lazy initialization.** `_queue`, `_started`, `_patched`, `_server_url` are module-managed state. Outside code reaching in to mutate them would break the module's invariants, so the underscore says "leave this alone."

**If another module needs to import it, it's not internal — drop the underscore.** The moment you write `from foo import _bar` in a different module, the underscore is a lie. Either the function is truly internal (don't import it) or it's a shared utility (move it to a common module and remove the prefix). When extracting helpers from one module into a shared `utils.py`, always drop the underscores — they were internal to the *old* module, not to the *new* one.

Do **not** prefix with underscore:

- **Module-level constants.** They're inert values. `UPPER_CASE` already conveys "constant"; the underscore adds noise without protecting anything. Use `MAX_RETRIES`, not `_MAX_RETRIES`; `OK`, not `_OK`.
- **Classes**, even ones used only inside the module. Privacy comes from *where the class lives* (don't re-export it from `__init__.py`, keep it next to its caller). The leading underscore on a class name is visual noise that doesn't enforce anything Python wouldn't already enforce by import path. Use `RequestTracer`, not `_RequestTracer`.

| Allowed | Disallowed |
|---------|------------|
| `def _build_summary(...)` (internal helper) | `MAX_RETRIES = 3` (constant — drop underscore) |
| `def _resolve_id(...)` (internal helper) | `OK = Response(...)` (constant — drop underscore) |
| `_queue: queue.Queue = ...` (mutable singleton) | `class _Tracer: ...` (class — drop underscore) |
| `_started: bool = False` (mutable singleton) | `_DEFAULT_HEADERS = {...}` (constant — drop underscore) |

Dunders (`__init__`, `__enter__`, …) are unaffected — those are Python's protocol, not the privacy convention.

## Import Hygiene

**Don't alias imports without a reason.** `from foo import bar as _bar` or
`from foo import bar as baz` obscures the real name. If there's no actual name
collision, use the original name.

**Shared utilities belong in a utility module.** When a helper is first written inside
the module that needs it, that's fine. The moment a *second* module imports it, move it
to a shared location (`utils.py`, `helpers.py`, etc.). Don't let `module_b` depend on
`module_a` just because `module_a` happened to define a generic string helper first.

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
- [ ] Module reads top-down (Clean Code's *newspaper metaphor*): public API on top, helpers below
- [ ] Leading underscores reserved for internal functions/methods and mutable singleton state — not constants, classes, or cross-module imports
- [ ] No `from foo import _bar` — if another module needs it, drop the underscore and move to a shared location
- [ ] No unnecessary import aliases (`from x import y as _y`)
- [ ] Function parameters and returns are annotated where the type is informative (no `Any`-everywhere on wrappers/passthroughs)
- [ ] Functions with 4+ parameters use keyword-only arguments
- [ ] No `typing.Union`, `typing.Optional`, `typing.List`, `typing.Dict` imports
- [ ] Class abbreviations use CamelCase (JsonParser, not JSONParser)
- [ ] Helper functions are prefixed with underscore
