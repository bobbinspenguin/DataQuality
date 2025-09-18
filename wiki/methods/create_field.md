```markdown
# `_create_field`
- **Short description:** Generate a derived column using a function or a literal value.
- **How it works:** Supports metadata entries with `function` names (e.g., `create_guid`, `get_date`) or literal `value`. The helper calls the function or assigns the literal and writes results to `output`. Optional `conditions` restrict which rows receive the generated value.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to add a field to. | `DataFrame` (input) |
| value | `str` or `None` | Literal value to assign when `function` not supplied. | `None` |
| function | `str` | Function name to generate values (e.g., `get_date`, `create_guid`). | `create_guid` |
| output | `str` | Name of the new column to create. | `new_anonymous_contact_id` |
| rule_name | `str` | Metadata rule name for logging. | `creating_annon_guid` |
| conditions | `list[dict]` | Optional list of conditions to restrict row-level creation. | `[{column: 'Annon', comparison: 'eq', value: 'Yes'}]` |
-
- **Example result:** `new_anonymous_contact_id` will contain GUIDs for rows where `Annon == 'Yes'`.

```
