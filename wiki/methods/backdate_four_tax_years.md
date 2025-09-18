```markdown
# `_backdate_four_tax_years`
- **Short description:** Backdate a date column to the 1st of April four tax years earlier.
- **How it works:** For `backdate_four_tax_years` metadata the method reads the `date` column (assumed already formatted as date), subtracts four tax years anchored to 1st April and writes the `output` column. Implementation may treat fiscal year rollover rules when month/day are considered.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| data_df | `DataFrame` | DataFrame to compute backdated values from. | `DataFrame` (input) |
| backdate_column | `str` | Source date column to use for backdating. | `start_date_as_date` |
| output_column_name | `str` | Name of the computed backdated output column. | `backdated_start_date` |
| rule_name | `str` | Metadata rule name for logging. | `backdating_start_date` |
-
- **Example result:** If `start_date_as_date` is `2024-08-15`, `backdated_start_date` becomes `2020-04-01` (example behaviour).

```
