# Custom Validation — Private Helper Methods

This file documents private helpers used by `custom_validation` rules found in `sample_metadata/custom_validation`.

---

## `_expect_column_values_to_be_unique_in_file`
- **Short description:** Detect duplicate values in the file for a given column and take configured action.
- **How it works:** Scans the `source_data_df` to find duplicated values in `column_name`. If duplicates are found, the method either returns `False` (file invalid), marks the rows with an error, or performs an action such as `reject_row` depending on the `action` parameter.
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to inspect for duplicates. | `DataFrame` (input) |
| column_name | `str` | Column to check uniqueness for. | `id` |
| action | `str` | Action to take when duplicates found (`reject_row`, `fail_file`, etc.). | `reject_row` |
| error_message | `str` or `None` | Custom error message to attach when duplicates are found. | `None` |
| rule_name | `str` | Metadata rule name for logging. | `validate_no_duplicates` |
- **Example result:** If two rows have `id = 123`, both rows will be flagged and the method returns `False` when the action indicates file-level rejection.

- **Example output (validation fail — duplicates):**

Input (excerpt):

| id | name |
|---:|---|
| 701 | `Alice` |
| 702 | `Bob` |
| 701 | `Alice Duplicate` |

Result: `id = 701` duplicates detected. `row_errors` entries for both offending rows and the method may return `False` if `action == 'reject_row'`.

---

## `_expect_column_values_to_not_be_null_custom`
- **Short description:** Null-check a list of columns but allow conditional custom error codes per condition.
- **How it works:** This variant of the non-null check accepts a `conditions` list where each condition may include a `custom_error_code`. The method evaluates conditions per row and for rows that match the condition but have nulls in the `columns` list, it attaches the specified `custom_error_code`. If no condition-specific code applies, `default_custom_error_code` is used. The `action` parameter controls what the method does with offending rows (e.g., `reject_row`).
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to validate nulls against with conditional error codes. | `DataFrame` (input) |
| columns | `list[str]` | Columns which must not be null when conditions match. | `['title', 'first_name', 'last_name']` |
| conditions | `list[dict]` | List of conditions that map to custom error codes per condition. | `[{column: 'is_approved', comparison: 'eq', value: 'Yes', custom_error_code: 'Whoops, something went wrong'}, {column: 'is_enabled', comparison: 'ne', value: 'No', custom_error_code: 'Whoops, something went wrong here too'}]` |
| default_error_code | `str` | Error message used when no condition-specific code applies. | `The contact details in this row are null and must be rejected.` |
| rule_name | `str` | Metadata rule name for logging. | `expect_contact_column_values_not_null` |
| action | `str` | Action to take on offending rows. | `reject_row` |
- **Example result:** A row with `is_approved == 'Yes'` and missing `last_name` will be flagged with `Whoops, something went wrong`. Rows that don't match any condition receive the default error code.

- **Example output (conditional null-check):**

Input (excerpt):

| user_id | is_approved | is_enabled | title | first_name | last_name |
|---:|---|---|---|---|---|
| 801 | `Yes` | `Yes` | `Mr` | `Tom` | `` |
| 802 | `No` | `Yes` | `Ms` | `` | `` |

Result: `801` flagged with `Whoops, something went wrong` (matches condition is_approved == 'Yes'). `802` flagged with default error code `The contact details in this row are null and must be rejected.` if it fails the columns check.

---

## `_expect_column_values`
- **Short description:** Evaluate a list of conditional checks and perform actions (drop, reject, fail) on matching rows.
- **How it works:** Receives `conditions` and an `action`. For each condition dict the method filters rows matching the comparisons (e.g., `column == value`) and either drops them from the returned DataFrame (`drop_row`), flags them (`reject_row`/`fail_row`), or returns an updated DataFrame depending on `action` semantics. It is a flexible rule executor used by simple conditional validations.
- **Example input parameters:**

| Parameter | Datatype | Description | Value |
|---|---:|---|---|
| source_data_df | `DataFrame` | DataFrame to evaluate conditional filters on. | `DataFrame` (input) |
| conditions | `list[dict]` | Conditions to match rows to act upon. | `[{column: 'type', comparison: 'eq', value: 'unknown'}]` |
| action | `str` | Action to take for matched rows (e.g., `drop_row`). | `drop_row` |
| rule_name | `str` | Metadata rule name for logging. | `expect_column_values_payment_type_conditional` |
- **Example result:** Rows where `type == 'unknown'` are dropped from the working DataFrame.

- **Example output (drop rows):**

Input (excerpt):

| account_id | type |
|---:|---|
| 901 | `known` |
| 902 | `unknown` |

Result: After `_expect_column_values(..., action='drop_row')` the returned DataFrame will only contain `account_id = 901`.

---

### Notes on error handling and actions
- `action` values commonly used: `drop_row`, `reject_row`, `fail_row`. Each action is implemented by higher-level code or the helper itself; documentation above describes the typical observable behaviour.
- Most helpers will append structured messages to `row_errors` for reporting — include row id, rule name, and custom error code when available.
