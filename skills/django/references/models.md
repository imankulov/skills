# Django Model Standards

## Base Classes

Use timestamped base models instead of bare `models.Model`:

- **MutableModel**: Tracks both `created_at` and `updated_at`
- **ImmutableModel**: Tracks only `created_at` (for append-only data)

Define these once in your project using callable defaults instead of `auto_now` /
`auto_now_add`:

```python
from django.db import models
from django.utils import timezone

class MutableModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class ImmutableModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
```

Why not `auto_now` / `auto_now_add`? They silently skip when you use queryset
`.update()` or raw SQL, they make the field non-editable (breaking admin and tests),
and their behavior diverges from what developers expect
([Django #22995](https://code.djangoproject.com/ticket/22995)). A callable `default=`
plus explicit `save()` override is transparent and works everywhere.

Note: pass `timezone.now` (the function), not `timezone.now()` (called immediately).

## Requirements

- Provide a descriptive docstring for each model class
- Implement `__str__` for all models
- Implement `get_absolute_url` when applicable (models with a detail view)
- Add indexes for frequently filtered/ordered fields, but don't add redundant indexes
  for fields that already have constraints (`unique=True`, `primary_key`, etc.)
- Do not specify `max_length` for CharField where the value is not obvious — PostgreSQL
  doesn't require it
- Use appropriate `on_delete` behavior for foreign keys

## Enum Fields

Use [`django-enum`](https://django-enum.readthedocs.io/en/stable/) instead of CharField
with choices:

```python
from django.db import models
from django_enum import EnumField

class RegistrationSource(models.TextChoices):
    """Types of registration sources."""
    ORGANIC = "organic", "Organic"
    GOOGLE_ADS = "google_ads", "Google Ads"
    REFERRAL = "referral", "Referral"

class User(MutableModel):
    """Application user."""

    name = models.CharField()
    email = models.EmailField()
    registration_source = EnumField(RegistrationSource, max_length=100)

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.email
```

Always set `max_length` for EnumField larger than the longest value to allow future
expansion. Define enums as separate classes inheriting from `TextChoices`.

## Schema Fields

For structured JSON data stored in a model field, use a schema field backed by Pydantic
instead of raw JSONField:

```python
from pydantic import BaseModel

class UserSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    theme: str = "light"
    language: str = "en"

class User(MutableModel):
    settings: UserSettings = SchemaField(UserSettings, default=UserSettings)
```

## Model Meta

Always use `db_table` to explicitly name the database table.

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| `CharField(max_length=255)` everywhere | PostgreSQL doesn't need it; arbitrary limits cause bugs | `CharField()` without max_length |
| `models.Model` as base | Loses audit timestamps | Use MutableModel or ImmutableModel |
| CharField with `choices=` | No type safety, no IDE support | EnumField with TextChoices class |
| JSONField for structured data | No validation, no schema | SchemaField with Pydantic model |
| Inline choice tuples | Hard to reference, no methods | Separate TextChoices class |
| `auto_now=True` / `auto_now_add=True` | Skips on `.update()`, makes field non-editable, surprising behavior | `default=timezone.now` + explicit `save()` override |
| `DateTimeField(default=timezone.now())` | Evaluates once at import time, all rows get the same timestamp | `default=timezone.now` (no parentheses — pass the callable) |
| Missing `__str__` | Admin and debugging are painful | Always implement `__str__` |
| Missing `db_table` in Meta | Django generates ugly names | Explicit `db_table` |
