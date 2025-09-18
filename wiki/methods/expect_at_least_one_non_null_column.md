```markdown
# `_expect_at_least_one_non_null_column`
- **Short description:** Ensure that at least one column from a group contains a non-null value for each row.
- **How it works:** Given a list of `columns`, the helper checks that for each row at least one of them is non-null/non-empty. If all are null, the row is flagged.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to check; at least one must be non-null per row. | `['email','phone']` |
| custom_error_message | `str` or `None` | Optional error message when all columns are null. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `expect_contact_present` |
-
- **Example result:** Rows without `email` and `phone` are flagged.
-
- **Example output (before → after):**

Input (excerpt):

| id | email | phone |
|---:|---|---|
| 1 | `` | `0123456789` |
| 2 | `` | `` |

Output (excerpt):

| id | email | phone | _validation_error |
|---:|---|---|---|
| 1 | `` | `0123456789` |  |
| 2 | `` | `` | `at least one contact method required` |

```
