```markdown
# `_expect_column_values_in_set`
- **Short description:** Validate that column values belong to an allowed set.
- **How it works:** For `in_set` metadata entries the method checks each value in the specified `columns` is present in the provided `allowed_values` set. If values fall outside the set the row is flagged. Optionally a `case_sensitive` flag controls matching behavior.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to check against allowed values. | `['status']` |
| allowed_values | `list[str]` | Set or list of allowed values. | `['Active','Inactive','Pending']` |
| case_sensitive | `bool` | Whether matching is case-sensitive. | `false` |
| custom_error_message | `str` or `None` | Optional custom error message for failures. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `expect_status_in_set` |
-
- **Example result:** Rows with `status == 'unknown'` are flagged as failing.
-
- **Example output (before → after):**

Input (excerpt):

| id | status |
|---:|---|
| 1 | `Active` |
| 2 | `unknown` |

Output (excerpt):

| id | status | _validation_error |
|---:|---|---|
| 1 | `Active` |  |
| 2 | `unknown` | `status must be one of [Active,Inactive,Pending]` |

```
