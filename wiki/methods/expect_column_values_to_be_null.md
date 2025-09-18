```markdown
# `_expect_column_values_to_be_null`
- **Short description:** Validate specified columns are null (used to ensure fields are blank when expected).
- **How it works:** Checks that listed `columns` contain null or empty values for all rows where the rule applies. Non-empty values produce a row-level failure.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns that must be null. | `['deprecated_field']` |
| rule_name | `str` | Metadata rule name for logging. | `expect_deprecated_field_null` |
-
- **Example result:** Rows with non-empty `deprecated_field` are flagged.
-
- **Example output (before → after):**

Input (excerpt):

| id | deprecated_field |
|---:|---|
| 1 | `` |
| 2 | `x` |

Output (excerpt):

| id | deprecated_field | _validation_error |
|---:|---|---|
| 1 | `` |  |
| 2 | `x` | `deprecated_field must be null` |

```
