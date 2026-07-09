# Parallel Processing Symmetry

When two systems (classifiers, processors, backends, pipelines) operate on the same input in parallel,
they should be symmetric across three dimensions: naming, abstraction level, and data shape.

## 1. Naming

Use a short, consistent prefix for each path across every layer — types, services, API, admin, CLI,
docs. The prefixes should be parallel in structure so the reader immediately sees the symmetry.

Audit all layers before finalizing. If one path uses `vector_score`, the other must use
`keyword_score`, not `estimated_score`.

```python
# types.py
class KeywordMatch(BaseModel): ...
class VectorMatch(BaseModel): ...

class SearchSummary(BaseModel):
    keyword_matches: list[KeywordMatch]
    keyword_score: float
    vector_matches: list[VectorMatch]
    vector_score: float

# services.py
def _keyword_search(query, corpus) -> ...: ...
def _vector_search(query, corpus) -> ...: ...
```

Bad — mixed naming breaks the parallel structure:

```python
class SearchRule(BaseModel): ...     # not prefixed
class Match(BaseModel): ...          # not prefixed

class SearchSummary(BaseModel):
    rules: list[SearchRule]          # "rules" vs "vector_matches"
    estimated_score: float           # "estimated" vs "vector"
    vector_matches: list[Match]
    vector_score: float
```

## 2. Abstraction level

Both paths handle their own edge cases, guards, and error handling internally. The caller sees them as
interchangeable black boxes with the same level of polish.

```python
def _keyword_search(query, corpus) -> tuple[list[KeywordMatch], float]:
    """Returns empty results if the corpus is empty."""
    if not corpus:
        return [], 0.0
    ...

def _vector_search(query, corpus) -> tuple[list[VectorMatch], float, str]:
    """Returns empty results if the API key is missing or the call fails."""
    if not config.EMBEDDING_API_KEY:
        return [], 0.0, ""
    try:
        return _vector_search_remote(query, corpus)
    except Exception as e:
        logger.warning("Vector search failed: {}", e)
        return [], 0.0, ""

# Caller — symmetric, no special handling for either path
keyword_matches, keyword_score = _keyword_search(query, corpus)
vector_matches, vector_score, vector_summary = _vector_search(query, corpus)
```

Bad — one path is a clean call, the other leaks error handling into the caller. The asymmetry makes the
vector path look fragile and the caller harder to read. Move the guard and the `try`/`except` inside
`_vector_search`:

```python
keyword_matches, keyword_score = _keyword_search(query, corpus)

vector_matches: list[VectorMatch] = []
vector_score = 0.0
vector_summary = ""
if config.EMBEDDING_API_KEY:
    try:
        vector_matches, vector_score, vector_summary = _vector_search(query, corpus)
    except Exception as e:
        logger.warning("Vector search failed: {}", e)
```

## 3. Data shapes

Parallel types should share the same structure where possible. When the same concept exists in both
paths, the types should share their core fields, with extras clearly additive.

```python
class KeywordMatch(BaseModel):
    field: str
    value: str
    confidence: Confidence
    document_count: int

class VectorMatch(BaseModel):
    field: str
    value: str
    confidence: Confidence
    reasoning: str              # vector-specific addition
    document_count: int
```

Bad — different shapes for the same concept make merging and comparison harder:

```python
class SearchRule(BaseModel):
    field: str
    values: list[str]           # grouped
    confidence: RuleConfidence

class Match(BaseModel):
    field: str
    value: str                  # individual
    confidence: float           # different type
    reasoning: str
    document_count: int
```
