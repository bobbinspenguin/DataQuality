# DataQualityLibrary - Method Summary

This document lists the methods implemented on the `DataQualityLibrary` class found in `DataQuality.ipynb`.
Each entry includes a brief description and whether the method is intended to be public or private (private methods start with `_`).

## Class

- **Class name**: `DataQualityLibrary`

## Methods

Below are the methods discovered and a short description of each.

- **`__init__`**: Constructor — initialise internal state. (public)
- **`log_processed_file`**: Log processed file metadata to `processed_files`. (public)
- **`_get_lookup_table`**: Retrieve a lookup table from the lakehouse. (private)
- **`toggle_verbose_logging`**: Toggle verbose logging flag on the instance. (public)
- **`processed_files_to_df`**: Convert `processed_files` list to a Spark DataFrame. (public)
- **`reset_error_logs`**: Reset `row_errors` to an empty list. (public)
- **`row_errors_to_df`**: Convert `row_errors` list to a Spark DataFrame. (public)
- **`method_calls_to_df`**: Convert `method_calls` list to a Spark DataFrame. (public)
- **`write_error_logs_to_lakehouse`**: Write `row_errors` to a Delta table. (public)
- **`_log_failed_rows`**: Collect and append failed-row log entries into `row_errors`. (private)
- **`file_validation`**: Validate file-level columns (mandatory/optional/ignore). (public)
- **`field_validation`**: Main entry for field-level validations; dispatches to internal checks. (public)
- **`_expect_column_values_between`**: Validate numeric range for column values. (private)
- **`_expect_column_values_in_set`**: Validate that column values belong to an allowed set. (private)
- **`_expect_column_values_to_be_null`**: Validate values are NULL according to rule. (private)
- **`_expect_column_values_to_not_be_null`**: Validate values are NOT NULL according to rule. (private)
- **`_expect_at_least_one_non_null_column`**: Ensure at least one column in a list has a non-null value. (private)
- **`_expect_relative_date`**: Validate dates relative to today (e.g., `today_or_earlier`). (private)
- **`_expect_format`**: Validate simple format/length checks. (private)
- **`_column_length_checks`**: Validate maximum lengths for string columns. (private)
- **`row_processing`**: Main entry for row-processing transformations; dispatches to helpers. (public)
- **`_format_data`**: Format/validate email, phone, postcode, date/datetime and return transformed DataFrame. (private)
- **`_concat_column_values`**: Concatenate multiple columns into one. (private)
- **`_copy_columns`**: Copy columns to new column names. (private)
- **`_set_default_column_value`**: Create defaulted columns when values are null or missing. (private)
- **`_remove_characters`**: Create new column with specified characters removed. (private)
- **`_backdate_four_tax_years`**: Backdate a date column to 1st April four years prior. (private)
- **`_add_date_part`**: Extract year/month/day parts from a date into a new column. (private)
- **`_match_to_optionset`**: Map labels to optionset values using metadata lookup. (private)
- **`_match_to_entity`**: Lookup and join data from a CRM entity table with configurable behaviours. (private)
- **`_match_to_external_reference`**: Join against external reference table to resolve IDs. (private)
- **`_match_to_type`**: Convenience wrapper to configure `_match_to_entity` for type lookups. (private)
- **`_convert_values`**: Create new columns by mapping/replacing values with configurable behaviours. (private)
- **`_create_field`**: Create derived/fixed-value or function-generated fields. (private)
- **`_first_non_null`**: Create a column containing the first non-null value from a list. (private)
- **`_create_conditional_column`**: Create a column based on if/then conditions with an else. (private)
- **`_remove_whitespace`**: Trim/ltrim/rtrim whitespace from a column. (private)
- **`custom_validation`**: Run custom validation rules. (public)
- **`_expect_column_values_to_be_unique_in_file`**: Check for duplicate values and optionally fail rows/files. (private)
- **`_expect_column_values_to_not_be_null_custom`**: Null-check with conditional custom error codes and actions. (private)
- **`_expect_column_values`**: Apply conditional actions (drop, fail, reject) based on column comparisons. (private)
- **`data_mapping`**: Main entry for mapping source data to output tables. (public)
- **`_persist_data`**: Generate stable row identifiers via hashing and uuid join. (private)
- **`_output_mapped_data`**: Write mapped output tables to CSV per metadata. (private)

## Notes

- Visibility is inferred by naming convention: methods beginning with `_` are considered private/internal.
- Descriptions are brief summaries derived from the docstrings and code in `DataQuality.ipynb`.

If you want a different layout (grouped by category, CSV export, or a full API markdown with signatures and parameters), tell me which format you prefer and I'll generate it.
