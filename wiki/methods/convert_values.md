```markdown
# `_convert_values`
- **Short description:** Map/replace column values using a replacements list and configurable behaviour for unexpected values.
- **How it works:** Reads `convert_values` metadata's `replaces` list and `behaviour` rules. For each column listed it maps `from` → `to`. If values outside the provided mapping exist, behaviour can be `fail_row` (mark or drop), `leave` (keep original), or `map_to_null` depending on implementation.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to transform/validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to apply value conversions to. | `['approved_phone']` |
| replaces | `list[dict]` | Replacement mappings: list of {from, to} dicts. | `[{from: 'TRUE', to: 'Yes'}, {from: 'FALSE', to: 'No'}]` |
| suffix | `str` | Suffix for created converted column names. | `_converted` |
| error_message | `str` or `None` | Custom error message for conversion failures. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `convert_true_yes` |
| behaviour | `str` | Behaviour when encountering unrecognised values (`keep_others`/`null_others`/`fail_row`). | `fail_row` |
-
- **Example result:** `approved_phone_converted` contains `Yes`/`No`. A row containing other values may be flagged as failed.

```
