---
paths:
  - "**/*.py"
---

# Link `herogold.orm` models with `Relationship`, not a foreign-key column

When a project's models use `herogold.orm`, link one model to another with `herogold.orm.Relationship`. Don't add an `<other>_id` field with `ForeignKey(get_foreign_key(Other))`.

```python
# Don't
used_by_id: int | None = Field(default=None, sa_column_args=(ForeignKey(get_foreign_key(Account)),))

# Do
used_by = Relationship(Account)
```

- `Relationship` keeps the link in its own association table, so the owner's table stays the same when a link is added later.
- If `Relationship` can't do what the code needs, for example taking the caller's session, follow the herogold-first steps: open an issue on HEROgold/HeroPy, patch around it locally, and mark the patch `# TODO(herogold#<n>)`. Don't fall back to a foreign-key column without saying so.
