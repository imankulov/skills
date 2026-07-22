# Django View Standards

For server-rendered views (not API endpoints). Use this for pages that return HTML
or redirects.

## Requirements

- Place view functions in `views.py`
- Use an auth decorator for views requiring login (e.g., `@auth_required_redirect`)
- Use typed request annotations (`AuthenticatedHttpRequest`)
- Return Django HTTP responses (`HttpResponseRedirect`, `HttpResponse`, etc.)

## URL Configuration

```python
# myapp/urls.py
from django.urls import path
from myapp.views import checkout, portal

app_name = "billing"

urlpatterns = [
    path("checkout", checkout, name="checkout"),
    path("portal", portal, name="portal"),
]

# project urls.py
from django.urls import include, path

urlpatterns = [
    path("billing/", include("myapp.urls")),
]
```

Always set `app_name` for URL namespacing.

## Example

```python
from django.http import HttpResponseRedirect
from myapp.services import create_checkout_session

@auth_required_redirect
def checkout(request: AuthenticatedHttpRequest):
    """Handle checkout for authenticated users."""
    checkout_url = create_checkout_session(user=request.auth)
    return HttpResponseRedirect(checkout_url)
```

## Testing

```python
def test_checkout_redirects(client_with_user):
    response = client_with_user.get("/billing/checkout")

    assert response.status_code == 302
    assert response.url.startswith("https://checkout.example.com")

def test_checkout_requires_auth(client):
    response = client.get("/billing/checkout")

    assert response.status_code == 302
    assert response.url == "/login"
```
