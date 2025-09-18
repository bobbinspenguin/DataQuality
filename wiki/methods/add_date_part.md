```markdown
# `_add_date_part`
- **Short description:** Extract day/month/year parts from a date into a new column.
- **How it works:** For `date_part` metadata entries the method extracts the requested `date_part` (`day`, `month`, `year`) from the specified `column` and writes the `output` column.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to extract date parts from. | `DataFrame` (input) |
| date_column | `str` | Column containing parsed date values. | `registration_date_as_date` |
| date_part | `str` | Which part to extract (`day`, `month`, `year`). | `day` |
| output_column | `str` | Name of the created column to hold extracted part. | `registration_day` |
| error_message | `str` or `None` | Optional custom error message for rows that cannot be parsed. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `get_starting_date` |
-
- **Example result:** `registration_day` contains the integer `15` for `2024-08-15`.

```
