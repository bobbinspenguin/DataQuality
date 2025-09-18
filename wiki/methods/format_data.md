```markdown
# `_format_data`
- **Short description:** Normalize and format date, datetime, email, phone and postcode columns and create suffixed output columns.
- **How it works:** The method inspects metadata entries of types `format_date`, `format_datetime`, `format_email_address`, `format_phone_number`, `format_post_code`. For each specified column it parses or normalises values (dates → `datetime` objects, emails → lowercased/trimmed, phones → digits-only/consistent formatting, postcodes → canonical spacing/uppercasing). It writes new columns using the `suffix` configured in metadata (e.g., `date_of_birth_as_date`). Side-effects may include adding new columns and normalising values in-place if metadata requested replacement.
-
- **Example input parameters:**
|
| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame containing the rows to format. | `DataFrame` (input) |
| format_name | `str` | The format to apply (email/phone/postcode/date/datetime). | `format_date` |
| format_pattern | `str` | Optional pattern used when parsing dates or datetimes. | `dd/MM/yyyy` |
| columns | `list[str]` | Columns to apply formatting to. | `['date_of_birth', 'registration_date']` |
| suffix | `str` | Suffix to append to generated output columns. | `_as_date` |
| conditions | `list` or `None` | Optional conditions restricting which rows receive formatting. | `None` |
| error_message | `str` or `None` | Optional custom error message to attach for failed rows. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `formatting_date_columns` |
-
- **Example result:** New columns `date_of_birth_as_date` and `registration_date_as_date` are added containing parsed dates. Invalid date strings may become null or produce row-level errors depending on implementation.
-
- **Example output (before → after):**

Input (excerpt):

| id | date_of_birth | registration_date |
|---:|---|---|
| 1 | `15/08/1980` | `01/01/2024` |
| 2 | `not a date` | `` |

Output (excerpt):

| id | date_of_birth | date_of_birth_as_date | registration_date | registration_date_as_date |
|---:|---|---:|---|---:|
| 1 | `15/08/1980` | `1980-08-15` | `01/01/2024` | `2024-01-01` |
| 2 | `not a date` | `null` | `` | `null` |

```
