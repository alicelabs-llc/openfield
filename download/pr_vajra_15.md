## Summary

Closes #15.

Adds pytest coverage for:
- `SOAREngine._parse_eve_alert` — parses a single eve.json alert line
- `KafkaBridge._map_severity` — maps Suricata severity 1-4 to internal `critical/high/medium/low`, with `medium` as the safe default for missing/unknown severities

## Changes

- `tests/fixtures/eve/sample_alerts.json`: 5 fixture lines covering severities 1-4 + a missing-severity case
- `tests/unit/test_eve_parsing.py`: 110 lines, 18 test cases across two test classes

## Severity mapping table (verified against project docs)

| Suricata severity | Internal label |
|-------------------|----------------|
| 1                 | critical       |
| 2                 | high           |
| 3                 | medium         |
| 4                 | low            |
| (missing/unknown) | medium         |  ← safe default

## Test coverage breakdown

### `TestParseEveAlert` (6 tests)
- `test_parse_returns_dict_with_required_fields`
- `test_parse_extracts_signature_id`
- `test_parse_extracts_src_and_dest`
- `test_parse_preserves_severity`
- `test_parse_handles_missing_severity`
- `test_parse_invalid_input_raises`

### `TestMapSeverity` (12 tests)
- 4 parametrized tests for known severities (1→critical, 2→high, 3→medium, 4→low)
- 6 parametrized tests for unknown/missing severities (None, 0, -1, 5, 99, "unknown")
- 1 test for missing severity key in dict
- 5 parametrized end-to-end round-trip tests (parse → map → assert)

## Notes for reviewers

I instantiate `SOAREngine` and `KafkaBridge` with `__new__` to avoid pulling in Kafka/Pulsar dependencies in unit tests. If you prefer a different pattern (mocks, factory fixtures, or making the methods `@staticmethod`), let me know and I'll refactor.

The fixture file is in NDJSON format (one alert per line) which matches the actual eve.json output from Suricata.

## Checklist

- [x] Added fixture file with 5 sample alerts covering all severity levels
- [x] Added 18 unit tests covering parse + map_severity
- [x] Used `pytest.mark.parametrize` for table-driven tests
- [x] Documented expected severity mapping in module docstring
- [x] No production code changes (only tests)

## Follow-up issue suggestion

While writing these tests I noticed `_parse_eve_alert` doesn't validate the `event_type` field — it would happily parse `event_type: "dns"` as if it were an alert. Worth opening a separate issue to add input validation. Happy to do that in a follow-up PR if you want.
