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
