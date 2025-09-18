# Row Processing — Private Helper Methods

This document describes the private helper methods used by `row_processing` actions. Each section shows a short description, how the method generally works, an example input (from `sample_metadata/row_processing`) and the expected change to the DataFrame.

---

## `_format_data`
- **Short description:** Normalize and format date, datetime, email, phone and postcode columns and create suffixed output columns.
- **How it works:** The method inspects metadata entries of types `format_date`, `format_datetime`, `format_email_address`, `format_phone_number`, `format_post_code`. For each specified column it parses or normalises values (dates → `datetime` objects, emails → lowercased/trimmed, phones → digits-only/consistent formatting, postcodes → canonical spacing/uppercasing). It writes new columns using the `suffix` configured in metadata (e.g., `date_of_birth_as_date`). Side-effects may include adding new columns and normalising values in-place if metadata requested replacement.
- **Example input parameters:**
- **Example input parameters:**

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
- **Example result:** New columns `date_of_birth_as_date` and `registration_date_as_date` are added containing parsed dates. Invalid date strings may become null or produce row-level errors depending on implementation.
- **Example result:** New columns `date_of_birth_as_date` and `registration_date_as_date` are added containing parsed dates. Invalid date strings may become null or produce row-level errors depending on implementation.

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

---

## `_concat_column_values`
- **Short description:** Concatenate multiple columns into one output column using a separator.
- **How it works:** For `concat` metadata entries it reads the listed `columns`, joins them using the `separator` (skipping or treating nulls per implementation), and writes the result into the `output` column. The method preserves original columns unless metadata includes a remove behaviour.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to transform. | `DataFrame` (input) |
| columns | `list[str]` | Columns to concatenate in order. | `['vector_id', 'active_channel', 'event_name']` |
| output_column | `str` | Name of the new concatenated column. | `campaign_activity_external_reference` |
| sep | `str` | Separator string used between values. | `' '` |
| rule_name | `str` | Metadata rule name for logging. | `concat_campaign_activity` |
- **Example result:** New column `campaign_activity_external_reference` containing strings like `"123 Online Purchase"` when source values exist.

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

---

## `_copy_columns`
- **Short description:** Copy or rename columns to new names.
- **How it works:** For `copy_columns` metadata entries the method iterates mappings in `copy_columns`, copies values from `column` to `new_column_name`. Typically used to rename a defaulted column into a canonical name (for example `ds_name_defaulted` → `data_source_name`).
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to transform. | `DataFrame` (input) |
| columns | `list[dict]` | List of mappings describing source column and new column name. | `[{column: 'ds_name_defaulted', new_column_name: 'data_source_name'}]` |
| rule_name | `str` | Metadata rule name for logging. | `copy_and_rename_data_source_name_column` |
- **Example result:** New column `data_source_name` created and populated with values from `ds_name_defaulted`.

- **Example output (before → after):**

Input (excerpt):

| ds_name | ds_name_defaulted |
|---|---|
| `Quickstart` | `Quickstart` |
| `` | `Quickstart` |

Output (excerpt):

| ds_name | ds_name_defaulted | data_source_name |
|---|---|---|
| `Quickstart` | `Quickstart` | `Quickstart` |
| `` | `Quickstart` | `Quickstart` |

---

## `_set_default_column_value`
- **Short description:** Populate missing columns with a default value and optionally create suffixed columns.
- **How it works:** For `default` metadata entries the method checks each listed `columns` and fills null or missing values with the `value` provided. When `suffix` is provided it creates a new column per original column using the suffix (e.g., `ds_name_defaulted`). The original columns may be kept or replaced depending on implementation.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| data_df | `DataFrame` | DataFrame to add defaulted columns to. | `DataFrame` (input) |
| columns | `list[str]` | Columns to apply the default value to (or create if missing). | `['ds_name']` |
| default_value | `Any` | Value to assign where the source value is null or missing. | `Quickstart` |
| suffix | `str` | Suffix to append to the created defaulted column names. | `_defaulted` |
| rule_name | `str` | Metadata rule name for logging. | `set_default_data_source` |
- **Example result:** Column `ds_name_defaulted` added with value `"Quickstart"` where `ds_name` was null or missing.

- **Example output (before → after):**

Input (excerpt):

| ds_name |
|---|
| `Quickstart` |
| `` |

Output (excerpt):

| ds_name | ds_name_defaulted |
|---|---|
| `Quickstart` | `Quickstart` |
| `` | `Quickstart` |

---

## `_remove_characters`
- **Short description:** Remove a list of characters from a source column and write to an output column.
- **How it works:** Reads the metadata `remove_characters` which include `characters` list and `output` name. The method strips all occurrences of the listed characters from the source column and writes the cleaned string to `output`.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| data_df | `DataFrame` | DataFrame to transform (source of column to clean). | `DataFrame` (input) |
| characters | `list[str]` | Characters to remove from the source column. | `['-']` |
| column_name | `str` | Name of the source column to clean. | `srt-cde` |
| output_column | `str` | Name of the output/cleaned column to create. | `sort_code` |
| rule_name | `str` | Metadata rule name for logging. | `format_sort_code` |
- **Example result:** For input `"12-34-56"` the output column `sort_code` will contain `"123456"`.

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

---

## `_backdate_four_tax_years`
- **Short description:** Backdate a date column to the 1st of April four tax years earlier.
- **How it works:** For `backdate_four_tax_years` metadata the method reads the `date` column (assumed already formatted as date), subtracts four tax years anchored to 1st April and writes the `output` column. Implementation may treat fiscal year rollover rules when month/day are considered.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| data_df | `DataFrame` | DataFrame to compute backdated values from. | `DataFrame` (input) |
| backdate_column | `str` | Source date column to use for backdating. | `start_date_as_date` |
| output_column_name | `str` | Name of the computed backdated output column. | `backdated_start_date` |
| rule_name | `str` | Metadata rule name for logging. | `backdating_start_date` |
- **Example result:** If `start_date_as_date` is `2024-08-15`, `backdated_start_date` becomes `2020-04-01` (example behaviour).

- **Example output (before → after):**

Input (excerpt):

| start_date_as_date |
|---|
| `2024-08-15` |
| `2021-03-10` |

Output (excerpt):

| start_date_as_date | backdated_start_date |
|---|---|
| `2024-08-15` | `2020-04-01` |
| `2021-03-10` | `2017-04-01` |

---

## `_add_date_part`
- **Short description:** Extract day/month/year parts from a date into a new column.
- **How it works:** For `date_part` metadata entries the method extracts the requested `date_part` (`day`, `month`, `year`) from the specified `column` and writes the `output` column.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to extract date parts from. | `DataFrame` (input) |
| date_column | `str` | Column containing parsed date values. | `registration_date_as_date` |
| date_part | `str` | Which part to extract (`day`, `month`, `year`). | `day` |
| output_column | `str` | Name of the created column to hold extracted part. | `registration_day` |
| error_message | `str` or `None` | Optional custom error message for rows that cannot be parsed. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `get_starting_date` |
- **Example result:** `registration_day` contains the integer `15` for `2024-08-15`.

- **Example output (before → after):**

Input (excerpt):

| registration_date_as_date |
|---|
| `2024-08-15` |
| `2023-12-01` |

Output (excerpt):

| registration_date_as_date | registration_day |
|---|---|
| `2024-08-15` | `15` |
| `2023-12-01` | `1` |

---

## `_convert_values`
- **Short description:** Map/replace column values using a replacements list and configurable behaviour for unexpected values.
- **How it works:** Reads `convert_values` metadata's `replaces` list and `behaviour` rules. For each column listed it maps `from` → `to`. If values outside the provided mapping exist, behaviour can be `fail_row` (mark or drop), `leave` (keep original), or `map_to_null` depending on implementation.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to transform/validate. | `DataFrame` (input) |
| columns | `list[str]` | Columns to apply value conversions to. | `['approved_phone']` |
| replaces | `list[dict]` | Replacement mappings: list of {from, to} dicts. | `[{from: 'TRUE', to: 'Yes'}, {from: 'FALSE', to: 'No'}]` |
| suffix | `str` | Suffix for created converted column names. | `_converted` |
| error_message | `str` or `None` | Custom error message for conversion failures. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `convert_true_yes` |
| behaviour | `str` | Behaviour when encountering unrecognised values (`keep_others`/`null_others`/`fail_row`). | `fail_row` |
- **Example result:** `approved_phone_converted` contains `Yes`/`No`. A row containing other values may be flagged as failed.

- **Example output (before → after):**

Input (excerpt):

| approved_phone |
|---|
| `TRUE` |
| `MAYBE` |

Output (excerpt):

| approved_phone | approved_phone_converted | row_error |
|---|---|---|
| `TRUE` | `Yes` | `` |
| `MAYBE` | `null` | `Unexpected value: MAYBE` |

---

## `_create_field` and `_create_conditional_column`
- **Short description:** Generate derived columns either with a function (e.g., uuid generation) or with conditional if/then rules.
- **How it works:** `_create_field` supports `function` entries (such as `create_guid`) — it calls the configured function and writes the `output`. `_create_conditional_column` evaluates `if_thens` blocks, applying `then` when conditions match, otherwise using `else`.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to add a field to. | `DataFrame` (input) |
| value | `str` or `None` | Literal value to assign when `function` not supplied. | `None` |
| function | `str` | Function name to generate values (e.g., `get_date`, `create_guid`). | `create_guid` |
| output | `str` | Name of the new column to create. | `new_anonymous_contact_id` |
| rule_name | `str` | Metadata rule name for logging. | `creating_annon_guid` |
| conditions | `list[dict]` | Optional list of conditions to restrict row-level creation. | `[{column: 'Annon', comparison: 'eq', value: 'Yes'}]` |

and

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to evaluate conditional rules on. | `DataFrame` (input) |
| if_thens | `list[dict]` | List of if/then blocks with `conditions` and `then` values or sources. | `[{conditions: [{column: 'Annon', comparison: 'eq', value: 'Yes'}], then: 'Unknown'}]` |
| else_value | `str` | Value to apply when no conditions match. | `''` |
| output | `str` | Name of the created column. | `create_annon_lastname` |
| rule_name | `str` | Metadata rule name for logging. | `create_none_annon_lastname` |
- **Example result:** `new_anonymous_contact_id` will contain GUIDs for rows where `Annon == 'Yes'`. `create_annon_lastname` will be `Unknown` for those rows.

- **Example output (before → after):**

Input (excerpt):

| Annon | LastName |
|---|---|
| `Yes` | `Smith` |
| `No` | `Jones` |

Output (excerpt):

| Annon | LastName | new_anonymous_contact_id | create_annon_lastname |
|---|---|---|---|
| `Yes` | `Smith` | `550e8400-e29b-41d4-a716-446655440000` | `Unknown` |
| `No` | `Jones` | `` | `` |

---

## `_first_non_null`
- **Short description:** Create a column that contains the first non-null value from a list of columns.
- **How it works:** Given `columns` and an `output` it scans columns left-to-right and picks the first non-null value into `output`.
- **Example input parameters:**
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to evaluate columns in left-to-right order. | `DataFrame` (input) |
| columns | `list[str]` | Ordered list of columns to inspect for the first non-null value. | `['create_annon_lastname', 'LastName']` |
| output | `str` | Name of the output column to create with the chosen value. | `LastName_anonymised` |
| rule_name | `str` | Metadata rule name for logging. | `first_non_null_annon_lastname` |
- **Example result:** `LastName_anonymised` will be `create_annon_lastname` when present, otherwise `LastName`.

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

---

## `_remove_whitespace`
- **Short description:** Trim and normalise whitespace in a column.
- **How it works:** Removes leading/trailing whitespace and optionally collapse internal whitespace depending on arguments. Writes back to the original or a new column.
- **Example input parameters:** Often used implicitly inside formatters; a metadata example may not exist in sample file but the method supports `format` operations.
