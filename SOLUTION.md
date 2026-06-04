cat > SOLUTION.md << 'EOF'
# Solution Notes

## The bug
`ChatRequest` in `src/api/models.py` used a mutable default (`filters: list = []`).
A mutable default is created once and shared across all instances, so filter
state leaked from one request into the next.

`tests/test_bug.py` caught this with: "State bleed detected! Got: ['leaked_filter']".

## The fix
Changed the field to use a factory so each request gets its own fresh list:

    filters: list = Field(default_factory=list)

(and imported `Field` from pydantic).

## Verification
- Before fix: 1 failed, 18 passed  (test_bug.py failing)
- After fix:  19 passed
- Reproduce:  python -m pytest tests/ -v
EOF
