```markdown
# `_expect_relative_date`
- **Short description:** Validate that a date column is within a relative offset from a reference date (e.g., within last N days/years).
- **How it works:** Parses the target `column` as dates and compares to `reference_date` (default `today`) applying `offset` and `unit` (`days`,`months`,`years`) with `direction` (`past`/`future`). Rows outside the relative range are flagged.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---:|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| column | `str` | Date column to validate. | `registration_date_as_date` |
| offset | `int` | Number of units for the window (e.g., 365 days). | `365` |
| unit | `str` | Unit for offset (`days`,`months`,`years`). | `days` |
| direction | `str` | `past` or `future` relative to `reference_date`. | `past` |
| reference_date | `date` or `None` | Anchor date (defaults to today). | `None` |
| rule_name | `str` | Metadata rule name for logging. | `expect_registration_recent` |
-
- **Example result:** Registrations older than 365 days are flagged.
-
- **Example output (before → after):**

Input (excerpt):

| id | registration_date_as_date |
|---:|---|
| 1 | `2024-08-01` |
| 2 | `2020-07-01` |

Output (excerpt):

| id | registration_date_as_date | _validation_error |
|---:|---|---|
| 1 | `2024-08-01` |  |
| 2 | `2020-07-01` | `registration_date must be within 365 days` |

```
