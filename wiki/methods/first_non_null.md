```markdown
# `_first_non_null`
- **Short description:** Create a column that contains the first non-null value from a list of columns.
- **How it works:** Given `columns` and an `output` it scans columns left-to-right and picks the first non-null value into `output`.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to evaluate columns in left-to-right order. | `DataFrame` (input) |
| columns | `list[str]` | Ordered list of columns to inspect for the first non-null value. | `['create_annon_lastname', 'LastName']` |
| output | `str` | Name of the output column to create with the chosen value. | `LastName_anonymised` |
| rule_name | `str` | Metadata rule name for logging. | `first_non_null_annon_lastname` |
-
- **Example result:** `LastName_anonymised` will be `create_annon_lastname` when present, otherwise `LastName`.
-
- **Example output (before → after):**

Input (excerpt):

| create_annon_lastname | LastName |
|---|---|
| `Unknown` | `Smith` |
| `` | `Jones` |

Output (excerpt):

| create_annon_lastname | LastName | LastName_anonymised |
|---|---|---|
| `Unknown` | `Smith` | `Unknown` |
| `` | `Jones` | `Jones` |

```
