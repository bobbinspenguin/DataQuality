```markdown
# `_expect_column_values_between`
- **Short description:** Check numeric ranges for specified columns.
- **How it works:** The method validates numeric columns are within `[min_value, max_value]` bounds, with optional `strict_min` and `strict_max` to enforce strict inequality. Non-numeric or out-of-range values produce row-level errors.
-
- **Example input parameters:**
|
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
-
- **Example result:** Negative `total_amount` values are flagged. Values exactly `0` would fail when `strict_min` is true.

```
