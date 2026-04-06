---
name: pytest
description: |
  Pytest testing standards emphasizing the AAA pattern, fixtures, and parametrize.
  Use when writing or reviewing Python tests with pytest, including Django tests.
  Covers fixture organization, database access patterns, API testing, and mock clients.
  Do NOT use for: JavaScript/TypeScript tests, unittest-style tests, or non-pytest
  frameworks.
---

# Pytest Standards

Opinionated testing conventions for pytest, with Django-specific patterns included.

## AAA Pattern (Arrange-Act-Assert)

Structure every test with clear separation:

1. **Arrange**: Set up test data and conditions (primarily using fixtures)
2. **Act**: Execute the code being tested
3. **Assert**: Verify the results

Never create empty Arrange, Act, or Assert sections. Skip them altogether if not needed.

```python
def test_user_service_create(sample_user, db_session):
    # Arrange
    service = UserService(db_session)

    # Act
    created_user = service.create(sample_user)

    # Assert
    assert created_user.id is not None
    assert created_user.name == sample_user.name
    assert created_user.created_at is not None
```

Multiple assertions are allowed in a single test if logically connected.

## Test Organization

- Store tests in `tests/` subdirectory within each module
- Name test files to match tested modules: `services.py` -> `tests/test_services.py`
- Always use flat pytest functions instead of test classes

## Fixture Discovery Order

Before creating a new fixture, check if one already exists:

1. Root `conftest.py`
2. Module's `tests/conftest.py`
3. Current test file
4. Create new fixture in appropriate `conftest.py` if necessary

Place fixtures in order of scope: session -> module -> function.

Fixtures shared across multiple test files in a module belong in `tests/conftest.py`,
not in individual test files.

## Parametrize

Use `@pytest.mark.parametrize` for testing multiple input/output combinations:

```python
@pytest.mark.parametrize(
    "full_name,email,expected_greeting",
    [
        ("John Smith", "john@example.com", "John"),
        ("Dr. Jane Doe", "jane@example.com", "Jane"),
        ("", "user@example.com", "user"),
    ],
)
def test_extract_greeting(name_provider, full_name, email, expected_greeting):
    # Act
    greeting = name_provider.extract_greeting(full_name, email)

    # Assert
    assert greeting == expected_greeting
```

## Running Tests

```bash
# All tests (excluding e2e)
uv run pytest -m "not e2e" -vv -s

# Specific test file
uv run pytest path/to/test_file.py -vv -s

# Specific test function
uv run pytest path/to/test_file.py::test_function_name -vv -s
```

Always use `-vv` (verbose) and `-s` (show stdout). Always exclude e2e tests by default
— they call external services and are slow/flaky. Only run e2e when changes directly
affect e2e-tested code.

## Django Database Access

Tests get database access in two ways:

1. **Via fixtures**: If a fixture depends on `db` (directly or transitively), the test
   automatically gets database access. No decorator needed.
2. **Via decorator**: If no fixtures bring `db` dependency, use `@pytest.mark.django_db`.

```python
# No decorator needed — client_with_user brings db via user fixture
def test_create_report_success(client_with_user):
    response = client_with_user.post("/api/v1/reports", ...)
    assert response.status_code == 200

# Decorator needed — client alone doesn't bring db
@pytest.mark.django_db
def test_create_report_requires_auth(client):
    response = client.post("/api/v1/reports", ...)
    assert response.status_code == 401
```

## Django API Testing

- Use the Django test client for API endpoints
- `client` fixture for unauthenticated requests
- `client_with_user` fixture for authenticated requests
- Never use `TestClient` from `ninja.testing`

For POST requests with JSON:

```python
response = client_with_user.post(
    "/api/v1/support/request",
    data={"text": "Help me"},
    content_type="application/json",
)
```

For database mutation tests, include ORM assertions:

```python
assert User.objects.get(id=user.id).settings.theme == "dark"
```

## Mock Client Testing

- Never modify global state in tests (avoid `make_empty()` or similar)
- Use class constants from mock clients directly
- Let test environment handle client configuration through `.env.test`
- Never mock `get_*_client()` factory functions — use the real mock client
- Mock clients store captured data — assert on those lists

```python
def test_event_is_captured(posthog_client):
    some_function_that_captures_event()

    assert len(posthog_client.events) == 1
    assert posthog_client.events[0]["event"] == "oauth_completed"
```

## Assertions for HTTP Responses

Short responses — assert the full body:

```python
assert response.status_code == 200
assert response.json() == {"status": "ok", "count": 3}
```

Long responses — assert on key fields:

```python
assert response.status_code == 200
data = response.json()
assert data["totalValue"]["numericValue"] == 200
assert data["pages"][0]["pagePath"] == "https://example.com/page2"
```

## E2E Tests

Mark tests that call external services with `@pytest.mark.e2e`:

```python
@pytest.mark.e2e
def test_llm_provider_extracts_greeting(llm_provider):
    greeting = llm_provider.guess_greeting("John Smith", "john@example.com")
    assert greeting == "John"
```

The marker alone is sufficient — no `os.environ` checks needed. CI skips them
automatically with `pytest -m "not e2e"`.

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Test classes | Unnecessary nesting, pytest is function-based | Flat test functions |
| Module-wide fixtures in test files | Hard to discover, duplicated | Move to `tests/conftest.py` |
| Mocking factory functions | Breaks dependency chain | Use `.env.test` with mock provider |
| Empty AAA sections | Noise | Skip the section entirely |
| `ninja.testing.TestClient` | Inconsistent with Django test client | `client` / `client_with_user` fixtures |
| Running e2e by default | Slow, flaky, external dependencies | `-m "not e2e"` |

## Verification

After writing tests, verify:

- [ ] Tests follow AAA pattern with clear separation
- [ ] Fixtures are in the right conftest.py (not in test files)
- [ ] Parametrize is used for multiple input/output combinations
- [ ] E2E tests are marked with `@pytest.mark.e2e`
- [ ] No test classes — only flat functions
- [ ] Database tests either use db-providing fixtures or `@pytest.mark.django_db`
