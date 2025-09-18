```markdown
# `_expect_column_values_to_not_be_null`
- **Short description:** Ensure specified columns do not contain null or missing values.
- **How it works:** Iterates over listed `columns` and flags rows where the value is null, empty string, or missing depending on the dataset semantics. Optionally `allow_blank` can permit empty strings.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to check for non-null values. | `['email']` |
| allow_blank | `bool` | Whether empty strings are permitted. | `false` |
| custom_error_message | `str` or `None` | Optional custom error message. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `expect_email_present` |
-
- **Example result:** Rows missing `email` are flagged.
-
- **Example output (before → after):**

Input (excerpt):

| id | email |
|---:|---|
| 1 | `john@example.com` |
| 2 | `` |

Output (excerpt):

| id | email | _validation_error |
|---:|---|---|
| 1 | `john@example.com` |  |
| 2 | `` | `email must not be null` |

```
