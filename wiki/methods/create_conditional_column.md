```markdown
# `_create_conditional_column`
- **Short description:** Create a column using conditional `if`/`then` blocks with an `else` fallback.
- **How it works:** Evaluates `if_thens` blocks from metadata; for the first matching `conditions` block the `then` value (literal or source column) is applied, otherwise `else` is used. Writes output to `output` column.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to evaluate conditional rules on. | `DataFrame` (input) |
| if_thens | `list[dict]` | List of if/then blocks with `conditions` and `then` values or sources. | `[{conditions: [{column: 'Annon', comparison: 'eq', value: 'Yes'}], then: 'Unknown'}]` |
| else_value | `str` | Value to apply when no conditions match. | `''` |
| output | `str` | Name of the created column. | `create_annon_lastname` |
| rule_name | `str` | Metadata rule name for logging. | `create_none_annon_lastname` |
-
- **Example result:** `create_annon_lastname` will be `Unknown` where `Annon == 'Yes'` and `''` otherwise.

```
