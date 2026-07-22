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
metadata:
  imankulov.skills-sh-group: Python
  imankulov.skills-sh-order: "10"
  imankulov.claude-display-name: Python
  imankulov.claude-category: development
  imankulov.claude-keywords: "python,agent-skills"
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
but contain no business logic. Entry points never import each other — they are peers
that all depend on services; cross-imports create circular dependencies and tight coupling.

**services.py** holds all business logic. Service functions are reusable across any
entry point — an API endpoint, a background task, a CLI command, and an admin action
can all call the same service function.

**Data layer** (models.py, types.py, const.py) defines data structures with zero
business logic. `const.py` must have no internal imports — it's safe to import from
anywhere.

Put all imports at the top of the module. Defer an import inside a function only to break
a circular dependency; needing this often means the module structure needs refactoring.

### Entry Point Naming Convention

Service functions own the base name. Entry points that wrap them add a suffix for their
layer, so `from myapp.services import create_user` works everywhere without aliasing.
Never use `import ... as` to work around a naming conflict; use the suffix instead.

| Layer | Suffix | Example |
|-------|--------|---------|
| Service (business logic) | *(none)* | `create_user()` |
| API endpoint | `_api` | `create_user_api()` |
| CLI command | `_cli` | `create_user_cli()` |
| Background task | `_task` | `create_user_task()` |

## Functions

- Type-annotate parameters and return values when the type carries information. If the only honest type is `Any` (a wrapper around an optional/dynamically-imported library, a generic decorator, a `**kwargs` passthrough), leave it unannotated — `Any` adds noise without helping the reader, the type checker, or the IDE.
- Google-style docstrings without type information (types live in the signature).
- For functions with more than 3 parameters, use keyword-only arguments (`*`).
- Prefix internal helper functions with underscore and keep their docstrings to one line.
- Order a file top-down like a newspaper (Robert C. Martin's *Clean Code*): public functions first, helpers below, a single-caller `_helper` directly under its caller. Group Pydantic/dataclass types near the top so they're defined before use.

```python
def process_user_data(*, user_id: int, name: str, email: str, age: int) -> UserData:
    """Process and validate user data.

    Args:
        user_id: Unique identifier for the user
        name: User's full name
        email: User's email address
        age: User's age in years

    Returns:
        Processed user data with validation status
    """
    ...

def _format_name(first: str, last: str) -> str:
    """Combine first and last name into full name."""
    return f"{first} {last}".strip()
```

## Leading Underscores

A single leading underscore says "internal — don't call or import this from outside this module." Reserve it for two cases where outside use would cause a real problem:

- **Internal functions and methods.** A `_helper` may skip validation the public API enforces, hold an invariant of the surrounding function, or change shape at any time.
- **Mutable singleton state used for lazy initialization** (`_queue`, `_started`, `_patched`, `_server_url`). Outside code mutating it would break the module's invariants.

If another module needs to import it, it's not internal — drop the underscore. `from foo import _bar` is a lie: either keep the function truly internal, or move it to a shared module and remove the prefix. When extracting a helper into a shared `utils.py`, drop the underscore — it was internal to the old module, not the new one.

Do not prefix module-level constants or classes. `UPPER_CASE` already conveys "constant"; class privacy comes from where the class lives (don't re-export it, keep it next to its caller). Use `MAX_RETRIES` and `RequestTracer`, not `_MAX_RETRIES` or `_RequestTracer`.

Dunders (`__init__`, `__enter__`, …) are Python's protocol, not this convention.

## Import Hygiene

Don't alias an import without an actual name collision — `from foo import bar as baz`
obscures the real name.

Shared utilities belong in a utility module. When a *second* module needs a helper first
written inside another module, move it to a shared location (`utils.py`, `helpers.py`).
Don't let `module_b` depend on `module_a` just because `module_a` defined a generic
helper first.

## Type Hints (PEP 604)

Use modern union syntax (`list[str]`, `dict[str, int] | None`). Never import `List`,
`Dict`, `Optional`, or `Union` from `typing` for basic types.

## Class Naming

Treat abbreviations as single words in CamelCase, capitalizing only the first letter:
`JsonParser`, `ApiClient`, `DbConnection`, `HttpResponse`, `SqlQuery` — not `JSONParser`.

## References

For detailed patterns on specific topics, load these as needed:

- [Data structures](references/data-structures.md) — Pydantic vs dicts, enums, interfaces, TypedDict
- [Module organization](references/module-organization.md) — types.py, const.py placement rules
- [Logical grouping](references/logical-grouping.md) — keeping fields, constants, and steps grouped by concern
- [Parallel symmetry](references/parallel-symmetry.md) — naming and shape when two systems process the same input
- [URL parsing](references/url-parsing.md) — furl for all URL manipulation

## Verification

After writing Python code, verify:

- [ ] Business logic lives in services.py; entry points are thin wrappers
- [ ] All imports at the top; module reads top-down (public API first, helpers below)
- [ ] Leading underscores only on internal functions/methods and mutable singleton state — never constants, classes, or cross-module imports
- [ ] Types annotated where informative (no `Any` on wrappers/passthroughs); 4+ parameters use keyword-only arguments
- [ ] Modern union syntax, no `typing.Union/Optional/List/Dict`
- [ ] Class abbreviations use CamelCase (JsonParser, not JSONParser)
- [ ] Fields, constants, and processing steps grouped by concern, in the same order everywhere
- [ ] Systems processing the same input in parallel share prefixes, guards, and data shapes
