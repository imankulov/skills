---
name: django
description: |
  Opinionated Django development patterns for well-structured, maintainable projects.
  Use when writing Django models, migrations, views, admin configuration, Celery
  tasks, or external service integrations.
  Also use when reviewing or refactoring Django code or creating new Django apps.
  Do NOT use for: Django Ninja API endpoints (use django-ninja skill), FastAPI, Flask,
  general Python (use python skill), test files (use pytest skill), or frontend code.
metadata:
  imankulov.skills-sh-group: Python
  imankulov.skills-sh-order: "20"
  imankulov.claude-display-name: Django
  imankulov.claude-category: development
  imankulov.claude-keywords: "django,agent-skills"
---

# Django Development Patterns

Opinionated conventions for Django projects. For app architecture and module
organization, see the **python** skill — those patterns apply to all Python projects.

## Celery Task Patterns

Task functions are suffixed with `_task`, calling the unsuffixed service function.
This keeps imports clean — `from myapp.services import execute_report` works without
aliasing.

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
avoids circular imports and makes task scheduling explicit at the call site. Keep
business logic in service functions so every entry point can reuse it; tasks only call
services.

### Schedule helpers

When several entry points need to create a pending record and schedule a task, extract a `schedule_*`
function into `tasks.py`. This is the one exception to "no logic in tasks.py": the function's single
responsibility is coupling record creation with task scheduling.

```python
# tasks.py
def schedule_refresh_all(user: User) -> RefreshOperation:
    """Create the pending record and schedule the task."""
    operation = create_pending_refresh_operation(user)
    refresh_all_task.delay(operation.id)
    return operation
```

Entry points call `schedule_refresh_all()` rather than duplicating the create-then-delay pattern.

## Cross-App Signals

When one app needs to react to events in another, use custom Django signals rather than direct imports
or model signals (`post_save` and friends).

- Define the signal in the emitting app's `signals.py`.
- Emit it from a service function, not from `Model.save()`. This gives control over when the signal
  fires and what data it carries.
- Define receivers in the listening app's `signals.py`, registered via `AppConfig.ready()`.

```python
# emitting app: accounts/signals.py
from django.dispatch import Signal
websites_updated = Signal()

# emitting app: accounts/services.py
websites_updated.send(sender=refresh_all, user=user, added=added)

# listening app: filtering/signals.py
from django.dispatch import receiver
from accounts.signals import websites_updated

@receiver(websites_updated)
def on_websites_updated(sender, user, added, **kwargs):
    ...

# listening app: filtering/apps.py
class FilteringConfig(AppConfig):
    def ready(self) -> None:
        import_module("filtering.signals")
```

Dependencies stay one-way: the listening app imports from the emitting app, never the reverse.

## Component References

For detailed patterns on specific Django components, load these references as needed:

- [Model standards](references/models.md) — base classes, EnumField, SchemaField, Meta
- [Migrations](references/migrations.md) — schema and data migration ordering,
  historical models, reversibility, and migration tests
- [Views](references/views.md) — Django view functions, URL configuration
- [Admin](references/admin.md) — list_display, search, filters, @admin.display
- [Service provider pattern](references/service-provider.md) — external service integrations with registry + factory

## Verification

After writing Django code, verify:

- [ ] Celery tasks are named `<service_function>_task`
- [ ] Tasks are scheduled from entry points, not services
- [ ] Repeated create-then-schedule logic is extracted into a `schedule_*` helper in tasks.py
- [ ] Cross-app reactions use custom signals emitted from services, not `post_save`
- [ ] Admin actions call service functions for mutations
- [ ] Persisted-field replacements include a data migration that preserves existing
      values, plus a migration test when loss would be user-visible
