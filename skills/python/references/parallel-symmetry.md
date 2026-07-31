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

class KeywordResult(BaseModel):
    matches: list[KeywordMatch] = []
    score: float = 0.0

class VectorResult(BaseModel):
    matches: list[VectorMatch] = []
    score: float = 0.0
    summary: str = ""

# services.py
def _keyword_search(query: str, corpus: list[Document]) -> KeywordResult: ...
def _vector_search(query: str, corpus: list[Document]) -> VectorResult: ...
```

## 2. Abstraction level

Both paths handle their own edge cases, guards, and error handling internally. The caller sees them as
interchangeable black boxes with the same level of polish.

```python
def _keyword_search(query: str, corpus: list[Document]) -> KeywordResult:
    """Returns an empty result if the corpus is empty."""
    if not corpus:
        return KeywordResult()
    ...

def _vector_search(query: str, corpus: list[Document]) -> VectorResult:
    """Returns an empty result if the API key is missing or the call fails."""
    if not config.EMBEDDING_API_KEY:
        return VectorResult()
    try:
        return _vector_search_remote(query, corpus)
    except Exception as exc:
        logger.warning("Vector search failed: %s", exc)
        return VectorResult()

# Caller — symmetric, no special handling for either path
keyword = _keyword_search(query, corpus)
vector = _vector_search(query, corpus)
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
