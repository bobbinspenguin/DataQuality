```markdown
# `_remove_whitespace`
- **Short description:** Trim and normalise whitespace in a column.
- **How it works:** Removes leading/trailing whitespace and optionally collapse internal whitespace depending on arguments. Writes back to the original or a new column.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to normalise whitespace for. | `DataFrame` (input) |
| column | `str` | Column to strip whitespace from. | `email` |
| how | `str` | Mode: `trim` (leading/trailing) or `collapse` (collapse internal whitespace). | `trim` |
-
- **Example result:** `email` value `' JOHN.SMITH@EXAMPLE.COM '` becomes `'JOHN.SMITH@EXAMPLE.COM'` (or lowercased by formatter when combined with `format`).

```
