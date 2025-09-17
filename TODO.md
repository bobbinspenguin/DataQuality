# Remove feed reference
* Change feed to datasource
* Change file/filename to table/table_name
* Rename parameters for public methods

# Single to multiple entities
* Update file_validation


# New
* Add source to target mapping (`data_mapping`)
* Add schema validation to work in a similar way to file validation
* Update `_get_lookup_table` to accept optional query as opposed to table name
* Add method to log information about processed and failed entities
* Add method to record the number of rows dropped in row processing

# Other
* return deep copies of class attributes where appropriate
* `_expect_relative_date` contains hardcoded variable `validation` - is this required or should it be parameterised?
* `_expect_format` accepts `format` parameter but does not use it?

