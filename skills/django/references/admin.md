# Django Admin Configuration

## Admin is an entry point, so keep it thin — and don't test it

`admin.py` gets the same treatment as `api.py`, `cli.py`, and `tasks.py`: a thin adapter
over `services.py`, thin enough that nothing in it is worth a test. Subclassing
`ModelAdmin`, listing `list_display` / `search_fields` / `list_filter` / `readonly_fields`
/ `autocomplete_fields` / `inlines`, a one-line `@admin.display` lookup, an overridden
`has_*_permission` — that's Django's own plumbing rendering a back-office page, not a
surface to test. Don't write tests for it, and don't add one just because a diff touched
`admin.py`.

The bar here is deliberately lower than for the rest of the codebase: the admin exists to
give operators and developers a working back office, not to ship a tested product surface.
So when a `ModelAdmin` grows something worth testing, that's the signal it has grown real
logic. Any computed value beyond a trivial field lookup, any rule an admin action would
enforce — move it into `services.py`, test it there, and have the admin method or action
call it, the same way an API handler calls a service instead of embedding the logic.

## Read-only and read-and-delete admins

When a service or a worker owns every field on a model, hand-editing a row in the admin
only drifts from whatever wrote it. Define two base classes once in the project's admin
utility module and subclass them, rather than hand-rolling `has_*_permission` overrides or
a `readonly_fields` list covering every field:

- **A read-and-delete admin** blocks add and change but leaves delete on Django's normal
  permission check: view and prune, don't edit. Prefer this one in most cases — even a
  fully worker-owned row sometimes needs clearing out when it's stuck or corrupt and no
  service-level delete or resync would replace it.
- **A read-only admin** blocks delete too. Reach for it only when a service replaces the
  rows wholesale, so a stray deletion would just be silently undone or would leave a gap
  until the next run. It pairs naturally with immutable, append-only models.

## Rendering JSON fields

A structured JSON field rendered as a plain `readonly_fields` entry shows up as an
unformatted `repr`. Exclude the raw field and list a `*_display` method instead, wrapping
a shared JSON-to-HTML helper in the project's utility module.

## Requirements

- Include all meaningful fields in `list_display`
- Implement `search_fields` for fields users commonly search
- Add `list_filter` for status fields, dates, and low-cardinality foreign keys
- Use `autocomplete_fields` for high-cardinality foreign keys (especially User)
- Set `readonly_fields` for `id`, `created_at`, `updated_at`
- Decorate custom display methods with `@admin.display`, always passing `description`,
  and `boolean=True` for methods returning a bool
- Add existing boolean fields directly to `list_display` rather than wrapping them in a method
- Pass values to `format_html` as positional args, never interpolated with f-strings, to avoid XSS
- Call service functions for mutations in admin actions rather than mutating models directly

## Example

```python
from django.contrib import admin
from django.utils.html import format_html
from myapp.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "is_active_display", "subscription_url_display")
    search_fields = ("email", "name")
    list_filter = ("is_active", "created_at")
    autocomplete_fields = ("owner",)
    readonly_fields = ("id", "created_at", "updated_at")

    @admin.display(description="Active Status", boolean=True)
    def is_active_display(self, obj: Customer) -> bool:
        return obj.project_set.count() > 0

    @admin.display(description="Subscription")
    def subscription_url_display(self, obj: Customer) -> str:
        return format_html(
            '<a href="{}" target="_blank">View Subscription</a>',
            obj.subscription_url,
        )
```
