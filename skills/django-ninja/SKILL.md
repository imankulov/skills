---
name: django-ninja
description: |
  Django Ninja API endpoint patterns including routers, authentication tiers, typed
  requests, and Pydantic input/output models.
  Use when writing or reviewing Django Ninja API endpoints, routers, or auth
  configuration. Also use when creating new API modules or adding endpoints.
  Do NOT use for: Django views that return HTML (use django skill), FastAPI, DRF
  (Django REST Framework), or general Django patterns.
---

# Django Ninja API Endpoints

Opinionated conventions for building APIs with Django Ninja.

## Structure

- Place all endpoints in `api.py` files
- Create a router per module: `router = Router(tags=["module_name"])`
- Use Django Ninja decorators: `@router.get()`, `@router.post()`, `@router.patch()`
- Entry points are thin wrappers — call service functions for business logic

### Naming Convention

API endpoint functions are suffixed with `_api` to avoid name collisions with the
service function they wrap. The service function owns the base name:

```python
# services.py — the real logic, no suffix
def create_user(*, email: str, name: str) -> User:
    ...

# api.py — thin wrapper, suffixed with _api
@router.post("/v1/users", auth=[require_user], response=UserResponse)
def create_user_api(request: AuthenticatedHttpRequest, input_data: CreateUserInput) -> UserResponse:
    user = create_user(email=input_data.email, name=input_data.name)
    return UserResponse.from_model(user)
```

This keeps the import clean — `from myapp.services import create_user` works without
aliasing. Never rename imports with `as` to resolve naming conflicts; use the suffix
instead.

## Authentication

Use two auth tiers:

- **`require_user`**: Endpoints that require authentication
- **`session_auth`**: Endpoints that work with both anonymous and authenticated users

Match the request type annotation to the auth level:

```python
from ninja import Router

router = Router(tags=["users"])

# Authenticated-only endpoint
@router.get("/v1/settings", auth=[require_user], response=UserSettings)
def get_user_settings(request: AuthenticatedHttpRequest) -> UserSettings:
    return request.auth.settings

# Mixed auth endpoint (anonymous + authenticated)
@router.post("/v1/feedback", auth=[session_auth], response=StatusResponse)
def create_feedback(
    request: AnyUserHttpRequest,
    input_data: FeedbackInput,
) -> StatusResponse:
    create_feedback_entry(user=request.auth, text=input_data.text)
    return StatusResponse(success=True)

# Checking auth state in mixed endpoints
@router.get("/v1/features", auth=[session_auth], response=Features)
def get_features(request: AnyUserHttpRequest) -> Features:
    if not request.auth.is_authenticated:
        return get_anonymous_features()
    return get_user_features(user_id=request.auth.id)
```

Access the user via `request.auth`, not `request.user`.

## Input/Output Models

- Use Pydantic models for input parameters, suffixed with `Input`
- Return typed response models
- Keep models in `types.py` unless used only in one endpoint

```python
# types.py
from pydantic import BaseModel
from datetime import datetime

class FeedbackInput(BaseModel):
    text: str
    page_url: str | None = None

class FeedbackResponse(BaseModel):
    id: int
    created_at: datetime
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Business logic in api.py | Can't reuse in tasks or CLI | Call service functions |
| `request.user` | Wrong attribute for Ninja auth | `request.auth` |
| Untyped request parameter | Loses auth type safety | `AuthenticatedHttpRequest` or `AnyUserHttpRequest` |
| Endpoint named same as service function | Import collision, forces ugly `as` alias | Suffix with `_api` |
| `from myapp.services import create_user as _create_user` | Obscures the real name, fragile | Name the endpoint `create_user_api` instead |
| Dict return values | No schema validation | Pydantic response models |

## Verification

After writing Django Ninja endpoints, verify:

- [ ] Endpoints live in `api.py` and call service functions
- [ ] Auth level matches request type annotation
- [ ] User is accessed via `request.auth`, not `request.user`
- [ ] Input models are suffixed with `Input`
- [ ] Return types are Pydantic models, not dicts
- [ ] Endpoint functions are suffixed with `_api`, no `import ... as` aliasing
