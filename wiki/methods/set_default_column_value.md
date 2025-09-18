```markdown
# `_set_default_column_value`
- **Short description:** Populate missing columns with a default value and optionally create suffixed columns.
- **How it works:** For `default` metadata entries the method checks each listed `columns` and fills null or missing values with the `value` provided. When `suffix` is provided it creates a new column per original column using the suffix (e.g., `ds_name_defaulted`). The original columns may be kept or replaced depending on implementation.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| data_df | `DataFrame` | DataFrame to add defaulted columns to. | `DataFrame` (input) |
| columns | `list[str]` | Columns to apply the default value to (or create if missing). | `['ds_name']` |
| default_value | `Any` | Value to assign where the source value is null or missing. | `Quickstart` |
| suffix | `str` | Suffix to append to the created defaulted column names. | `_defaulted` |
| rule_name | `str` | Metadata rule name for logging. | `set_default_data_source` |
-
- **Example result:** Column `ds_name_defaulted` added with value `"Quickstart"` where `ds_name` was null or missing.
-
- **Example output (before → after):**

Input (excerpt):

| ds_name |
|---|
| `Quickstart` |
| `` |

Output (excerpt):

| ds_name | ds_name_defaulted |
|---|---|
| `Quickstart` | `Quickstart` |
| `` | `Quickstart` |

```
