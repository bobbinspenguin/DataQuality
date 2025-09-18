```markdown
# `_remove_characters`
- **Short description:** Remove a list of characters from a source column and write to an output column.
- **How it works:** Reads the metadata `remove_characters` which include `characters` list and `output` name. The method strips all occurrences of the listed characters from the source column and writes the cleaned string to `output`.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| data_df | `DataFrame` | DataFrame to transform (source of column to clean). | `DataFrame` (input) |
| characters | `list[str]` | Characters to remove from the source column. | `['-']` |
| column_name | `str` | Name of the source column to clean. | `srt-cde` |
| output_column | `str` | Name of the output/cleaned column to create. | `sort_code` |
| rule_name | `str` | Metadata rule name for logging. | `format_sort_code` |
-
- **Example result:** For input `"12-34-56"` the output column `sort_code` will contain `"123456"`.
-
- **Example output (before → after):**

Input (excerpt):

| srt-cde |
|---|
| `12-34-56` |
| `98-76` |

Output (excerpt):

| srt-cde | sort_code |
|---|---|
| `12-34-56` | `123456` |
| `98-76` | `9876` |

```
