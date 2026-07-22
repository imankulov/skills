---
name: django-ninja
description: |
  Django Ninja API endpoint patterns including routers, authentication tiers, typed
  requests, and Pydantic input/output models.
  Use when writing or reviewing Django Ninja API endpoints, routers, or auth
  configuration. Also use when creating new API modules or adding endpoints.
  Do NOT use for: Django views that return HTML (use django skill), FastAPI, DRF
  (Django REST Framework), or general Django patterns.
metadata:
  imankulov.skills-sh-group: Python
  imankulov.skills-sh-order: "30"
  imankulov.claude-display-name: Django Ninja
  imankulov.claude-category: development
  imankulov.claude-keywords: "django,ninja,agent-skills"
---

# Django Ninja API Endpoints

Opinionated conventions for building APIs with Django Ninja.

## Structure

- Place all endpoints in `api.py` files
- Create a router per module: `router = Router(tags=["module_name"])`
- Keep endpoints as thin wrappers that call service functions for all business logic

### Naming Convention

Suffix API endpoint functions with `_api` so the service function they wrap keeps
the base name, and import the service directly without an `as` alias:

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

## Authentication

Use two auth tiers, and match the request type annotation to the tier:

- **`require_user`** with `AuthenticatedHttpRequest`: endpoints that require authentication
- **`session_auth`** with `AnyUserHttpRequest`: endpoints serving both anonymous and authenticated users

Access the user via `request.auth`, not `request.user`. In mixed-auth endpoints, branch
on `request.auth.is_authenticated`:

```python
@router.get("/v1/features", auth=[session_auth], response=Features)
def get_features(request: AnyUserHttpRequest) -> Features:
    if not request.auth.is_authenticated:
        return get_anonymous_features()
    return get_user_features(user_id=request.auth.id)
```

## Input/Output Models

- Use Pydantic models for input parameters, suffixed with `Input`
- Return typed Pydantic response models, never dicts
- Keep models in `types.py` unless used only in one endpoint
