```markdown
# `_expect_column_values_to_not_be_null_custom`
- **Short description:** Custom non-null validation allowing custom value definitions for 'null' (e.g., `N/A`,`unknown`).
- **How it works:** Similar to standard non-null checks but accepts `null_values` list to treat certain literal strings as null. Flags rows where values are not allowed to be considered present per `allow_blank`.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to check. | `['address_line_2']` |
| null_values | `list[str]` | Strings to treat as null. | `['N/A','unknown']` |
| allow_blank | `bool` | Whether empty strings considered valid. | `false` |
| rule_name | `str` | Metadata rule name for logging. | `expect_address_present_or_known` |
-
- **Example result:** Rows with `address_line_2 == 'N/A'` are treated as null and flagged accordingly.
-
- **Example output (before → after):**

Input (excerpt):

| id | address_line_2 |
|---:|---|
| 1 | `N/A` |
| 2 | `Flat 2` |

Output (excerpt):

| id | address_line_2 | _validation_error |
|---:|---|---|
| 1 | `N/A` | `address_line_2 must not be null` |
| 2 | `Flat 2` |  |

```
