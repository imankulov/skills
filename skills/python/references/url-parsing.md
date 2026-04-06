# URL Parsing with furl

Use [furl](https://github.com/gruns/furl) for all URL manipulation. Never use string
concatenation or `urllib.parse`.

## Building URLs

```python
from furl import furl

url = furl("https://api.example.com")
url.path.segments = ["v1", "users"]
url.args["active"] = "true"
final_url = str(url)  # https://api.example.com/v1/users?active=true
```

## Parsing URLs

```python
from furl import furl

f = furl("https://example.com/api?key=value")
path = f.path       # /api
params = dict(f.args)  # {"key": "value"}
scheme = f.scheme    # https
host = f.host        # example.com
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| `f"{base}/v1/users?active=true"` | No escaping, breaks on special chars | `furl` |
| `urllib.parse.urlparse` | Verbose, error-prone API | `furl` |
| `urllib.parse.urlencode` | Manual assembly | `furl.args` |
| Manual query string building | Encoding bugs | `furl.args["key"] = value` |

Always validate URL schemes when parsing user-provided URLs.
