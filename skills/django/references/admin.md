# Django Admin Configuration

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
