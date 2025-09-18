```markdown
# `_copy_columns`
- **Short description:** Copy or rename columns to new names.
- **How it works:** For `copy_columns` metadata entries the method iterates mappings in `copy_columns`, copies values from `column` to `new_column_name`. Typically used to rename a defaulted column into a canonical name (for example `ds_name_defaulted` → `data_source_name`).
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to transform. | `DataFrame` (input) |
| columns | `list[dict]` | List of mappings describing source column and new column name. | `[{column: 'ds_name_defaulted', new_column_name: 'data_source_name'}]` |
| rule_name | `str` | Metadata rule name for logging. | `copy_and_rename_data_source_name_column` |
-
- **Example result:** New column `data_source_name` created and populated with values from `ds_name_defaulted`.
-
- **Example output (before → after):**

Input (excerpt):

| ds_name | ds_name_defaulted |
|---|---|
| `Quickstart` | `Quickstart` |
| `` | `Quickstart` |

Output (excerpt):

| ds_name | ds_name_defaulted | data_source_name |
|---|---|---|
| `Quickstart` | `Quickstart` | `Quickstart` |
| `` | `Quickstart` | `Quickstart` |

```
