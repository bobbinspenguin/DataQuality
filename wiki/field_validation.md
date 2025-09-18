# Field Validation — Private Helper Methods

This document covers the private helper methods that implement field-level validation rules. Each entry includes a short description, how the method works, example input parameters (from `sample_metadata/field_validation`) and example results.

---

## `_expect_column_values_to_not_be_null`
- **Short description:** Ensure specified columns contain non-null values.
- **How it works:** For `expect_column_values_to_not_be_null` rules the method checks every listed column for null or empty values. If `conditions` are provided the check is applied only for rows matching those conditions. When nulls are found the method either flags rows (into `row_errors`) or ``rejects``/``drops`` rows depending on the higher-level action.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| null_check_df | `DataFrame` | DataFrame to validate (filtered when `conditions` provided). | `DataFrame` (input) |
| columns | `list[str]` | Columns to check for non-null values. | `['id', 'title', 'first_name', 'last_name', 'date_of_birth']` |
| custom_error_message | `str` or `None` | Optional custom error message used for flagged rows. | `None` |
| rule_name | `str` | Name of the metadata rule used for logging. | `expect_contact_column_values_not_null` |
| conditions | `list` or `None` | Optional list of conditions to restrict rows the check applies to. | `None` |
- **Example result:** Rows with null `id` or `last_name` are flagged. If action is `reject_row`, those rows are recorded in `row_errors` and excluded or marked for rejection.

- **Example output (validation pass):**

Input (excerpt):

| id | title | first_name | last_name | date_of_birth |
|---:|---|---|---|---|
| 1 | `Mr` | `John` | `Smith` | `1980-08-15` |
| 2 | `Ms` | `Jane` | `Jones` | `1990-01-10` |

Result: both rows pass — no `row_errors` appended.

- **Example output (validation fail):**

Input (excerpt):

| id | title | first_name | last_name | date_of_birth |
|---:|---|---|---|---|
| 3 | `` | `Sam` | `` | `2000-05-05` |

Result: row flagged; `row_errors` entry like `{row_id: 3, rule: 'expect_contact_column_values_not_null', error: 'Missing last_name'}` and row rejected if action `reject_row`.

---

## `_expect_column_distinct_values_to_be_in_set` / `_expect_column_values_in_set`
- **Short description:** Ensure column values are part of an allowed set of values.
- **How it works:** The method takes a `values` list and checks that each non-null value in the specified columns is one of the allowed values. It raises or flags rows with invalid values, optionally attaching a `custom_error_code` message.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to validate against the allowed set. | `['age_bracket']` |
| custom_error_message | `str` | Optional error message to use when values are not in the set. | `Age bracket must be one of...` |
| value_set | `list[str]` | Allowed values for the column(s). | `['Under 18','18-24','25-34','35-44','45-54','55-64','65+','75+']` |
| rule_name | `str` | Metadata rule name for logging. | `expect_age_bracket_in_set` |
- **Example result:** Rows where `age_bracket` contains `"Unknown"` are flagged with the provided custom error code.

- **Example output (validation pass):**

Input (excerpt):

| account_id | age_bracket |
|---:|---|
| 101 | `25-34` |
| 102 | `45-54` |

Result: pass.

- **Example output (validation fail):**

Input (excerpt):

| account_id | age_bracket |
|---:|---|
| 103 | `Unknown` |

Result: `row_errors` entry: `{row_id: 103, rule: 'expect_age_bracket_in_set', error: 'Age bracket must be one of...'}`.

---

## `_expect_column_values_to_be_between` / `_expect_column_values_between`
- **Short description:** Check numeric ranges for specified columns.
- **How it works:** The method validates numeric columns are within `[min_value, max_value]` bounds, with optional `strict_min` and `strict_max` to enforce strict inequality. Non-numeric or out-of-range values produce row-level errors.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to validate (casts columns to numeric for checks). | `DataFrame` (input) |
| columns | `list[str]` | Columns to apply the range check to. | `['total_amount']` |
| min_value | `int` or `float` | Lower bound value (None to skip lower bound). | `0` |
| max_value | `int` or `float` | Upper bound value (None to skip upper bound). | `1000000` |
| strict_min | `bool` | If true use strict > comparison for the minimum. | `true` |
| strict_max | `bool` | If true use strict < comparison for the maximum. | `false` |
| custom_error_message | `str` or `None` | Optional custom error message to use for failures. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `expect_total_amount_between` |
- **Example result:** Negative `total_amount` values are flagged. Values exactly `0` would fail when `strict_min` is true.

- **Example output (validation pass):**

Input (excerpt):

| sales_id | total_amount |
|---:|---:|
| 201 | 100.00 |
| 202 | 5000.00 |

Result: pass.

- **Example output (validation fail):**

Input (excerpt):

| sales_id | total_amount |
|---:|---:|
| 203 | -10.00 |
| 204 | 0.00 |

Result: `203` flagged (negative); `204` flagged if `strict_min` true.

---

## `_expect_column_values_to_be_null`
- **Short description:** Ensure the listed columns are null (e.g., for candidate rows that shouldn't have a matched id).
- **How it works:** Checks that columns are null for rows that match optional conditions, otherwise flags rows. Useful for ensuring no pre-existing matched id is present when inserting new records.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| null_check_df | `DataFrame` | DataFrame to validate (optionally filtered by `conditions`). | `DataFrame` (input) |
| columns | `list[str]` | Columns expected to be null. | `['matched_id']` |
| custom_error_message | `str` | Error message used when non-null values are found. | `A record with this id already exists` |
| rule_name | `str` | Metadata rule name for logging. | `expect_matched_id_null` |
| conditions | `list` or `None` | Optional conditions to restrict application of the check. | `None` |
- **Example result:** Rows where `matched_id` is not null are flagged with the custom error code.

- **Example output (validation fail):**

Input (excerpt):

| sales_id | matched_id |
|---:|---|
| 301 | `NULL` |
| 302 | `12345` |

Result: `302` flagged with error `A record with this id already exists`.

---

## `_expect_at_least_one_non_null_column`
- **Short description:** Ensure at least one column in a list is non-null for each row.
- **How it works:** Scans the provided `columns` per row and verifies at least one contains a non-null/meaningful value. If all values are null/blank the row is flagged with `custom_error_code`.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| one_non_null_df | `DataFrame` | DataFrame to validate (optionally filtered by `conditions`). | `DataFrame` (input) |
| columns | `list[str]` | Columns where at least one must be non-null per row. | `['email_formatted', 'mobile_formatted', 'phone_formatted', 'postcode']` |
| custom_error_message | `str` | Custom error message for rows missing values in all listed columns. | `At least one of Email, Phone Mobile, Phone Home or Postcode must be populated` |
| rule_name | `str` | Metadata rule name for logging. | `expect_at_least_one_contact_detail` |
| conditions | `list` or `None` | Optional conditions to restrict the check. | `None` |
- **Example result:** Rows with all four columns null are flagged with the provided error message.

- **Example output (validation fail):**

Input (excerpt):

| user_id | email_formatted | mobile_formatted | phone_formatted | postcode |
|---:|---|---|---|---|
| 401 | `` | `` | `` | `` |

Result: `401` flagged with `At least one of Email, Phone Mobile, Phone Home or Postcode must be populated`.

---

## `_expect_relative_date`
- **Short description:** Validate date columns relative to today (e.g., must be today or in the past).
- **How it works:** The helper interprets `time` or `time_check_type` metadata and compares column date values to the current date. It supports checks like `today_or_earlier`. Non-conforming dates are flagged with `custom_error_code`.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to validate containing date columns. | `DataFrame` (input) |
| columns | `list[str]` | Columns to compare relative to today's date. | `['date_of_registration']` |
| custom_error_message | `str` | Optional custom error message used for failures. | `date_of_registration must be today or in the past` |
| time_check_type | `str` | Type of relative check (e.g., `today_or_earlier` / `today_or_later`). | `registration_date_as_date` |
| rule_name | `str` | Metadata rule name for logging. | `expect_relative_registration_date` |
- **Example result:** Future `date_of_registration` values (after today) are flagged.

- **Example output (validation fail):**

Input (excerpt):

| account_id | date_of_registration |
|---:|---|
| 501 | `2026-01-01` |

Result: `501` flagged with `date_of_registration must be today or in the past`.

---

## `_expect_format`
- **Short description:** Validate column formatting and length constraints.
- **How it works:** Checks formats such as `email`, `phone` or enforces `length`. The `format` metadata may be a string keyword (like `any`, `email`, `phone`) or a regex. Implementation may normalise values first and then validate.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to validate/format. | `DataFrame` (input) |
| columns | `list[str]` | Columns to validate the format of (e.g., email). | `['email']` |
| format | `str` | Format type to validate (e.g., `email`, `phone`, `any`). | `email` |
| length | `int` or `None` | Expected string length for format checks (when applicable). | `None` |
| rule_name | `str` | Metadata rule name for logging. | `format_email_address` |
| custom_error_message | `str` or `None` | Optional custom error message to use for failures. | `None` |
- **Example result:** `email_formatted` contains normalised email addresses or null for invalid strings; invalid rows may be flagged.

- **Example output (before → after):**

Input (excerpt):

| contact_id | email |
|---:|---|
| 601 | ` JOHN.SMITH@EXAMPLE.COM ` |
| 602 | `not-an-email` |

Output (excerpt):

| contact_id | email | email_formatted | row_error |
|---:|---|---|---|
| 601 | ` JOHN.SMITH@EXAMPLE.COM ` | `john.smith@example.com` | `` |
| 602 | `not-an-email` | `null` | `Invalid email format` |
