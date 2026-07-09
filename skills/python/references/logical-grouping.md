# Grouping by Logical Concern

When code contains items from multiple logical groups — fields, constants, or processing steps — keep
each group's items contiguous. Don't interleave items from different concerns.

This applies to Pydantic models, ORM models, module-level constants, constructor and factory calls,
function bodies, admin fieldsets, and table columns.

## Rules

- Identify the logical groups (e.g. shared metadata, billing, one group per backend or classifier).
- Keep each group's items contiguous.
- Use the same group order everywhere: type definition, constructor calls, function body, display code.
- When a function processes several groups, process them in the order the type defines them. The reader
  should follow the flow top-to-bottom without jumping around.
- Add a short comment per group when the grouping isn't obvious from the names.

## Fields

```python
class SearchSummary(BaseModel):
    # Shared
    total_documents: int

    # Keyword backend
    keyword_matches: list[KeywordMatch]
    keyword_score: float

    # Vector backend
    vector_matches: list[VectorMatch] = []
    vector_score: float = 0.0
    vector_summary: str = ""


# The constructor follows the same order
summary = SearchSummary(
    total_documents=total,
    keyword_matches=keyword_matches,
    keyword_score=keyword_score,
    vector_matches=vector_matches,
    vector_score=vector_score,
    vector_summary=vector_summary,
)
```

Bad — a shared field splits a logical group apart:

```python
class SearchSummary(BaseModel):
    keyword_matches: list[KeywordMatch]
    total_documents: int          # shared field breaks the keyword group apart
    keyword_score: float
    vector_matches: list[VectorMatch] = []
```

## Function bodies

The type defines shared → keyword → vector, so the function processes them in that order:

```python
def build_summary(query: str) -> SearchSummary:
    corpus = load_corpus()

    # Shared
    total = len(corpus)

    # Keyword backend
    keyword_matches, keyword_score = _keyword_search(query, corpus)

    # Vector backend
    vector_matches, vector_score, vector_summary = _vector_search(query, corpus)

    return SearchSummary(...)
```

Bad — the processing order doesn't match the type definition, so the reader has to jump around:

```python
def build_summary(query: str) -> SearchSummary:
    keyword_matches, keyword_score = _keyword_search(query, corpus)
    total = len(corpus)
    vector_matches, vector_score, vector_summary = _vector_search(query, corpus)
    indexed_at = corpus.indexed_at
```

## Constants

```python
# HIGH confidence: exact signature matches
HIGH_SCORE_THRESHOLD = 0.20

# MEDIUM confidence: statistical anomalies
MEDIUM_SCORE_THRESHOLD = 0.05
MEDIUM_CLUSTER_THRESHOLD = 0.02

# LOW confidence: weak source signals
LOW_SOURCE_THRESHOLD = 0.10
```

Bad — arbitrary order, no grouping, redundant prefixes:

```python
SUSPICIOUS_SCORE_THRESHOLD = 0.20
SUSPICIOUS_DURATION_THRESHOLD = 15.0
HIGH_CONFIDENCE_SCORE_THRESHOLD = 0.20
MEDIUM_CONFIDENCE_CLUSTER_THRESHOLD = 0.02
LOW_CONFIDENCE_SOURCE_THRESHOLD = 0.10
MEDIUM_CONFIDENCE_SCORE_THRESHOLD = 0.05
```
