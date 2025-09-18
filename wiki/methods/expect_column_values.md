```markdown
# `_expect_column_values`
- **Short description:** General-purpose column value expectation with configurable checks.
- **How it works:** A flexible validator that can apply different checks specified in metadata such as `in_set`, `between`, `not_null`, `format` by delegating to the specific expectation helpers or by running compound checks. Produces row-level failures when any configured check fails.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| column | `str` | Column to validate. | `status` |
| checks | `list[dict]` | List of checks to perform (e.g., {type: 'in_set', allowed_values: [...] }). | `[{type:'in_set', allowed_values:['A','B']}]` |
| rule_name | `str` | Metadata rule name for logging. | `expect_status_general` |
-
- **Example result:** Runs sub-checks and flags rows failing any condition.
-
- **Example output (before → after):**

Input (excerpt):

| id | status |
|---:|---|
| 1 | `A` |
| 2 | `X` |

Output (excerpt):

| id | status | _validation_error |
|---:|---|---|
| 1 | `A` |  |
| 2 | `X` | `status did not pass required checks` |

```
