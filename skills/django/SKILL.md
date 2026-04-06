---
name: django
description: |
  Opinionated Django development patterns for well-structured, maintainable projects.
  Use when writing Django models, views, admin configuration, Celery tasks, or
  external service integrations.
  Also use when reviewing or refactoring Django code or creating new Django apps.
  Do NOT use for: Django Ninja API endpoints (use django-ninja skill), FastAPI, Flask,
  general Python (use python skill), test files (use pytest skill), or frontend code.
---

# Django Development Patterns

Opinionated conventions for Django projects. For app architecture and module
organization, see the **python** skill — those patterns apply to all Python projects.

## Celery Task Patterns

Task functions are suffixed with `_task`, calling the unsuffixed service function.
This keeps imports clean — `from myapp.services import execute_report` works without
aliasing. Never use `import ... as` to resolve naming conflicts; use the suffix instead.

```python
from myapp.services import execute_report, fail_report

@celery_app.task(bind=True)
def execute_report_task(self, report_id: int) -> None:
    """Execute report generation asynchronously."""
    try:
        execute_report(report_id)
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            fail_report(report_id=report_id, error_message=str(exc))
        raise
```

Schedule tasks from entry points (api.py, admin.py), not from service functions. This
avoids circular imports and makes task scheduling explicit at the call site.

| Avoid | Why | Instead |
|-------|-----|---------|
| Scheduling tasks inside services.py | Circular imports, hidden side effects | Schedule from entry points after calling the service |
| Business logic inside tasks.py | Can't reuse in other entry points | Call service functions from tasks |
| Task named same as service function | Import collision, forces `as` alias | Suffix with `_task` |
| `from myapp.services import execute_report as _execute` | Obscures the real name | Name the task `execute_report_task` |

## Component References

For detailed patterns on specific Django components, load these references as needed:

- [Model standards](references/models.md) — base classes, EnumField, SchemaField, Meta
- [Views](references/views.md) — Django view functions, URL configuration
- [Admin](references/admin.md) — list_display, search, filters, @admin.display
- [Service provider pattern](references/service-provider.md) — external service integrations with registry + factory

## Verification

After writing Django code, verify:

- [ ] Celery tasks are named `<service_function>_task`
- [ ] Tasks are scheduled from entry points, not services
- [ ] Admin actions call service functions for mutations
