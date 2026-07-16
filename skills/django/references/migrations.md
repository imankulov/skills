# Django migration standards

Treat persisted data as part of the application contract. A clean model definition is
not enough when existing rows still use the previous shape.

## Replacing a persisted field

Use an expand, migrate, contract sequence:

1. Add the new schema while the old field still exists.
2. Copy or transform existing values with `RunPython`.
3. Remove the old field only after the data operation.

These steps may live in one migration when Django executes them safely in order. Split
them when deployment compatibility, table-lock duration, or a circular relationship
requires separate releases.

Never read runtime model classes in a data migration. Use
`apps.get_model("app_name", "ModelName")` so the migration sees the historical model
state. Keep the transformation self-contained because application services and model
methods will evolve while old migrations must continue to run.

```python
def copy_legacy_values(apps, schema_editor):
    Settings = apps.get_model("accounts", "Settings")
    for settings in Settings.objects.exclude(legacy_value=""):
        settings.new_value = settings.legacy_value
        settings.save(update_fields=["new_value"])
```

## Reversibility

Provide a reverse function when the old representation can faithfully express the new
one. If reversal is inherently lossy, use `migrations.RunPython.noop` only after making
that limitation explicit in the migration and accepting that rollback cannot restore
the old data.

When the new shape is richer than the old one, define a deterministic reverse policy.
For example, restore the configured default rather than selecting an arbitrary child.

## Foreign keys introduced during replacement

When a parent gains a foreign key to a newly created child model:

1. Create the child model.
2. Add the nullable parent foreign key.
3. Create child rows and populate the parent key in `RunPython`.
4. Remove the legacy field.

Keep the new foreign key nullable if “no configured value” is valid. Use database
constraints for invariants the database can express, and service/admin validation for
cross-row invariants that cannot be represented by a normal constraint.

## Migration tests

Write a migration test when existing user or configuration data could be lost or
silently reinterpreted:

1. Migrate to the old state with `MigrationExecutor`.
2. Create rows through the historical app registry.
3. Migrate to the new state.
4. Assert the complete new representation, including relationships and structured
   fields.
5. Restore the graph's leaf migrations in `finally` so later tests see the normal
   schema.

Test the reverse migration when rollback is supported and non-trivial. The test should
prove preserved meaning, not merely that the migration completes.

## Verification

- [ ] New schema exists before the data copy runs
- [ ] Data functions use historical models from `apps`
- [ ] Every persisted legacy value has a deterministic destination
- [ ] Reverse behavior is implemented or explicitly documented as irreversible
- [ ] Foreign keys are populated only after both sides exist
- [ ] A migration test covers user-visible or configuration data preservation
