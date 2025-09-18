```markdown
# `_expect_column_values_to_be_unique_in_file`
- **Short description:** Ensure values in the specified column are unique across the file.
- **How it works:** Checks for duplicates in the given `column` and flags rows sharing duplicate values. Optionally `ignore_nulls` can skip null values when checking uniqueness.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| column | `str` | Column to ensure uniqueness for. | `external_reference` |
| ignore_nulls | `bool` | Whether to ignore nulls when checking uniqueness. | `true` |
| rule_name | `str` | Metadata rule name for logging. | `expect_external_reference_unique` |
-
- **Example result:** Rows with duplicate `external_reference` are flagged.
-
- **Example output (before → after):**

Input (excerpt):

| id | external_reference |
|---:|---|
| 1 | `A` |
| 2 | `A` |

Output (excerpt):

| id | external_reference | _validation_error |
|---:|---|---|
| 1 | `A` | `duplicate value in external_reference` |
| 2 | `A` | `duplicate value in external_reference` |

```
