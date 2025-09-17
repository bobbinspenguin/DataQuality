# Remove feed reference
* Change feed to datasource
* Change file/filename to table/table_name

# Single to multiple entities
* Update file_validation to be entity_validation or schema_validation


# New
* Add source to target mapping
* Add schema validation to work in a similar way to file validation
* Update `_get_lookup_table` to accept optional query as opposed to table name
* Add method to log information about processed and failed entities
* Add method to record the number of rows dropped in row processing

# Other
* `_expect_relative_date` contains hardcoded variable `validation` - is this required or should it be parameterised?
* `_expect_format` accepts `format` parameter but does not use it?

