# Django Admin Configuration

## Requirements

- Include all meaningful fields in `list_display`
- Implement `search_fields` for fields users commonly search
- Add `list_filter` for status fields, dates, and low-cardinality foreign keys
- Use `autocomplete_fields` for high-cardinality foreign keys (especially User)
- Set `readonly_fields` for `id`, `created_at`, `updated_at`
- Use `@admin.display` decorator for custom display methods
- Always provide `description` parameter in `@admin.display`
- Use `boolean=True` for methods returning boolean values
- Never create wrapper methods for boolean fields just to render a checkmark

## Example

```python
from django.contrib import admin
from django.utils.html import format_html
from myapp.models import Customer, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "is_active_display", "subscription_url_display")
    search_fields = ("email", "name")
    list_filter = ("is_active", "created_at")
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_display", "status")
    search_fields = ("id", "customer__email")
    list_filter = ("status", "created_at")
    autocomplete_fields = ("customer",)
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "created_at"

    @admin.display(description="Total Amount")
    def total_display(self, obj: Order) -> str:
        return f"${obj.total:.2f}"
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Wrapper method for existing boolean field | Unnecessary code, no display improvement | Add field directly to `list_display` |
| Missing `@admin.display` | No column header, no boolean checkmarks | Always decorate custom methods |
| `format_html` with f-strings | XSS vulnerability | Use positional args in `format_html()` |
| Direct model mutation in admin actions | Bypasses business logic | Call service functions |
