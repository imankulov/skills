# External Service Provider Pattern

A pattern for integrating external services (LLMs, payment processors, email senders,
analytics clients) with a clean interface, mock for testing, and factory for
configuration.

## Structure

```
myapp/providers/
├── __init__.py          # Factory function with registry
├── interface.py         # Abstract base class
├── mock.py              # Mock implementation for testing
├── real.py              # Production implementation
└── tests/
    ├── test_mock.py
    └── test_real.py
```

## Interface

```python
# interface.py
import abc
from typing import Self

class IEmailSender(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_config(cls) -> Self:
        """Create instance from application configuration."""

    @abc.abstractmethod
    def send(self, *, to: str, subject: str, body: str) -> None:
        """Send an email."""
```

## Factory with Registry

```python
# __init__.py
from functools import cache

from myapp import config
from myapp.providers.interface import IEmailSender
from myapp.providers.mock import MockEmailSender
from myapp.providers.smtp import SmtpEmailSender

EMAIL_SENDERS = {
    "smtp": SmtpEmailSender,
    "mock": MockEmailSender,
}

@cache
def get_email_sender() -> IEmailSender:
    """Get the configured email sender instance."""
    provider_name = config.EMAIL_SENDER
    if provider_name not in EMAIL_SENDERS:
        raise ValueError(f"Unknown email sender: {provider_name}")
    return EMAIL_SENDERS[provider_name].from_config()
```

## Mock Implementation

```python
# mock.py
from loguru import logger
from typing import Self
from myapp.providers.interface import IEmailSender

class MockEmailSender(IEmailSender):
    @classmethod
    def from_config(cls) -> Self:
        return cls()

    def send(self, *, to: str, subject: str, body: str) -> None:
        logger.debug(f"Mock email to={to} subject={subject}")
```

Use `loguru.logger.debug()` in mock implementations for transparency during testing.

## High-Level Service Functions

Wrap the provider with service functions using a distinct prefix:

```python
# services.py
from myapp.providers import get_email_sender

def email_send(*, to: str, subject: str, body: str) -> None:
    """Send an email using the configured provider."""
    get_email_sender().send(to=to, subject=subject, body=body)
```

Use a consistent prefix matching the service name (`email_send`, `email_send_bulk`,
`posthog_capture`, `posthog_identify`) to avoid collisions and make usage discoverable.

## Configuration

```python
# config.py
EMAIL_SENDER = env.get("EMAIL_SENDER", "mock")

# .env.test
EMAIL_SENDER=mock
```

Default to `"mock"` in config so tests work without external services.

## Testing

- Split tests by provider: `test_mock.py`, `test_real.py`
- Mark real provider tests with `@pytest.mark.e2e`
- Create fixtures using `.from_config()` classmethod
- Skip trivial mock tests — mock implementations are simple enough

```python
# test_real.py
import pytest
from myapp.providers.real import SmtpEmailSender

@pytest.fixture
def smtp_sender():
    return SmtpEmailSender.from_config()

@pytest.mark.e2e
def test_smtp_sends_email(smtp_sender):
    # Act
    smtp_sender.send(to="test@example.com", subject="Test", body="Hello")

    # Assert — check external system or mock SMTP server
```

## Checklist

- [ ] Abstract interface with `from_config()` classmethod
- [ ] Registry dict mapping provider names to classes
- [ ] `@cache` on factory function
- [ ] Mock implementation with `loguru.logger.debug()`
- [ ] Config defaults to `"mock"`
- [ ] `.env.test` uses mock provider
- [ ] E2E tests marked with `@pytest.mark.e2e`
