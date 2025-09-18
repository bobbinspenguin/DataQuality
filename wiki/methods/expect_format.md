```markdown
# `_expect_format`
- **Short description:** Validate a column value matches an expected format (regex or named format types like email/postcode).
- **How it works:** Uses either a provided regex `pattern` or a `format_type` (e.g., `email`, `uk_postcode`) to validate values. Non-matching rows are flagged with optional custom messages.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| column | `str` | Column to validate. | `email` |
| pattern | `str` or `None` | Regex pattern for validation. | `^[^@\s]+@[^@\s]+\.[^@\s]+$` |
| format_type | `str` or `None` | Named format type (email/postcode/phone). | `email` |
| case_sensitive | `bool` | Whether regex matching is case-sensitive. | `false` |
| custom_error_message | `str` or `None` | Optional error message. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `expect_valid_email` |
-
- **Example result:** Invalid emails are flagged; valid ones pass.
-
- **Example output (before → after):**

Input (excerpt):

| id | email |
|---:|---|
| 1 | `a@b.com` |
| 2 | `not-an-email` |

Output (excerpt):

| id | email | _validation_error |
|---:|---|---|
| 1 | `a@b.com` |  |
| 2 | `not-an-email` | `email does not match expected format` |

```
