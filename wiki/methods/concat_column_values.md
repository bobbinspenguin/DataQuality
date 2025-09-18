```markdown
# `_concat_column_values`
- **Short description:** Concatenate multiple columns into one output column using a separator.
- **How it works:** For `concat` metadata entries it reads the listed `columns`, joins them using the `separator` (skipping or treating nulls per implementation), and writes the result into the `output` column. The method preserves original columns unless metadata includes a remove behaviour.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to transform. | `DataFrame` (input) |
| columns | `list[str]` | Columns to concatenate in order. | `['vector_id', 'active_channel', 'event_name']` |
| output_column | `str` | Name of the new concatenated column. | `campaign_activity_external_reference` |
| sep | `str` | Separator string used between values. | `' '` |
| rule_name | `str` | Metadata rule name for logging. | `concat_campaign_activity` |
-
- **Example result:** New column `campaign_activity_external_reference` containing strings like `"123 Online Purchase"` when source values exist.
-
- **Example output (before → after):**

Input (excerpt):

| vector_id | active_channel | event_name |
|---|---|---|
| 123 | `Online` | `Purchase` |
| 456 | `` | `Signup` |

Output (excerpt):

| vector_id | active_channel | event_name | campaign_activity_external_reference |
|---|---|---|---|
| 123 | `Online` | `Purchase` | `123 Online Purchase` |
| 456 | `` | `Signup` | `456  Signup` |

```
