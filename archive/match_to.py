    def _match_to_optionset(self, source_data_df: DataFrame, entity_name: str, optionset_name: str, source_column: str, output_column: str, custom_error: str, behaviour: str, rule_name:str) -> DataFrame:
        """Gets the optionset value for a corresponding label.
        Queries the Dynamics OptionSetMetadata entity to retrieve the value and 
        lable columns for a specified entity. These are then compared to the supplied
        source column in the dataframe, and a new column is created containing the 
        option set values for use in the matching process.

        Args:
            source_data_df (DataFrame): Spark dataframe containing source data.
            entity_name (str): Name of the Dynamics entity to reference.
            optionset_name (str): Name of the option set to reference.
            source_column (str): Name of the column containing the value to search for.
            output_column (str): Name of the new column to be created.
            custom_error (str): Optional custom error message from the rule metadata.
            behaviour (str): Action to take if the match fails, e.g. fail_row or return_null
            rule_name (str): Name of the metadata rule that called this function

        Returns:
            source_data_df (DataFrame): Tranformed dataframe with the additional column.
        """
        
        if behaviour:
            behaviour = behaviour["found_none_behaviour"]
        else:
            behaviour = 'fail_row'

        validation = "Match to Optionset"
        # Query the GlobalOptionSetMetadata table for the supplied optionset
        optionset_df = (
            spark
            .table(f"{self.environment}_GlobalOptionSetMetadata")
            .where(f"EntityName = '{entity_name}' AND OptionSetName = '{optionset_name}'")
        )

        optionset_data = {row.Option : row.LocalizedLabel for row in optionset_df.collect()}
        
        # Spark UDF to map localizedlabel to optionsetvalue
        def label_to_value(column_value):
            """Spark UDF swaps the label for the optionset value."""
            for key, value in optionset_data.items():
                if value.lower() == column_value:
                    return key


            return None

        # Register the UDF
        label_to_value_udf = F.udf(label_to_value, StringType())

        # Create output column containing optionset values for the column values
        source_data_df = source_data_df.withColumn(output_column, label_to_value_udf(F.lower(F.col(source_column))))

        # Only retrieve matches for rows in which the source column contains a value    
        no_match_df = source_data_df.where((F.col(output_column).isNull()) & (F.col(source_column).isNotNull()))

        if not no_match_df.isEmpty():
            if behaviour == "fail_row":
                
                for row in no_match_df.collect():
                    standard_error = f"The value in '{source_column}' does not match an option in the optionset '{optionset_name}' in entity '{entity_name}'."
                    error_message = custom_error if custom_error else standard_error

                    self._log_failed_rows(no_match_df, validation, rule_name, "row processing", error_message)
            elif behaviour == "return_null":
                source_data_df = source_data_df.withColumn(output_column, F.lit(None))
            else:
                if self.verbose_logging:
                    self.logger.warning(f"Received unexpected behaviour {behaviour}")


        return source_data_df
        
    def _match_to_entity(self, source_data_df: DataFrame, entity: str, match_filters: list[dict], behaviour: dict, output_columns: list[dict], validate_null: bool, conditions: list[dict], custom_error: str, validation:str, rule_name:str)-> DataFrame:
        """Function to return the specified columns from a single matching row in the existing SCRM data
        The function takes a set of filter columns and values to find the precise row required
        Multiple columns can be output as determined by the output_columns dictionary
        Where no match or multiple matches are found, the behaviours dictionary determines the desired outcome

        Args:
            source_data_df (DataFrame): Spark dataframe containing source data.
            entity_name (str): Name of the Dynamics entity to reference.
            match_filters (list[dict]): List of filters. 
                The dictionary contains a filter_on field and a filter_by_ field which can be a column or string
            behaviour (dict): A dictionary of actions to take if the resulting lookup returns no rows or multiple rows
                The default behaviours are:
                    found_none_behaviour: fail_row
                    found_multiple_behaviour: fail_row
            output_columns (list[dict]): A list of columns to output from the matched row, and their alias
            validate_null (bool): Whether a null condition should be included in the validation (e.g. null may be a valid value, such as in title)
            conditions:list[dict]: Conditions under which the value is to be assigned for the row
            error_message(str): Error message to output (optional) 
            validation(str): The type of validation to use in error logging, required as match_to_entity is called by other functions
            rule_name (str): Name of the metadata rule that called this function

        Returns:
            source_data_df (DataFrame): Tranformed dataframe with the additional column.
        """
        # Get error messages
        no_match_entity_error = None
        no_match_entity_error = custom_error if custom_error else f"No matching record can be found in the {entity} table in the SCRM that match this row. Create a matching row and resubmit"
        multiple_match_entity_error = None
        multiple_match_entity_error = custom_error if custom_error else f"Multiple matching records in {entity} were returned for this row. Fix the duplicated rows in the SCRM and resubmit."

        # Create an expression to check if all the output columns are null
        # This is checked to see if there is a match in SCRM
        check_matched_columns = [F.col(col["column_name_in_scrm"]).isNull() for col in output_columns]
        check_match_columns_expr = None
        for expression in check_matched_columns:
            if check_match_columns_expr is None:
                check_match_columns_expr = expression
            else:
                check_match_columns_expr = check_match_columns_expr & expression

        # Get the fully qualified table
        entity_table = f"{self.environment}_{entity}"

        # Build the join condition using either column or value
        join_condition = None
        for match in match_filters:
            entity_col = match.get("filter_on")
            source_col = match.get("filter_by_column")
            static_val = match.get("filter_by_value")
                        
            if source_col:
                # Create an expression to see if the input column is not null
                # This is used to see if there is a match in SCRM
                check_match_columns_expr = check_match_columns_expr & F.col(source_col).isNotNull()
                
                condition = f"LOWER(source_data_df.`{source_col}`) = LOWER(entity.{entity_col})"
            else:
                # Lower the static value if it is a string else leave it as is if it is another
                #  data type such as an integer or float
                expression = f"LOWER('{static_val}')" if isinstance(static_val, str) else f"{static_val}"
                condition = f"LOWER(entity.{entity_col}) = {expression}"
        
            join_condition = join_condition + " AND " + condition if join_condition else condition

        # Build the list of columns to select and their alias to be used in source_data_df 
        select_columns = None
        for output in output_columns:
            output_column = output.get("column_name_in_scrm")
            output_alias = output.get("output")

            select_column = f"entity.{output_column} AS {output_alias}"

            select_columns = select_columns + "," + select_column if select_columns else select_column

        # Convert source_data_df to a view to allow joining with the entity table
        source_data_df.createOrReplaceTempView("source_data_df")

        # Build the query
        sql_query = f"""
            SELECT source_data_df.*, {select_columns}, entity.createdon
            FROM source_data_df
            LEFT JOIN {entity_table} AS entity
            ON {join_condition}
            """
        # Execute the query, returning the source_data_df with the columns from entity as specified    
        matched_df = self._spark.sql(sql_query)

        # Handle behaviours
        # Set defaults
        found_none_behaviour = None
        found_multiple_behaviour = None
        valid_found_none_behaviours = ["fail_row", "return_null"]
        valid_found_multiple_behaviours = ["fail_row", "oldest", "newest", "any"]

        # overwrite with values for this rule iteration if present and valid
        if behaviour:
            found_none_behaviour = behaviour.get("found_none_behaviour", None)
            found_multiple_behaviour = behaviour.get("found_multiple_behaviour", None)

        if found_none_behaviour is None or found_none_behaviour not in valid_found_none_behaviours:
            found_none_behaviour = "fail_row"

        if found_multiple_behaviour is None or found_multiple_behaviour not in valid_found_multiple_behaviours:
            found_multiple_behaviour = "fail_row"

        # Found none behaviour. 
        # Since the join returns null in the columns if no match is found, 
        # there is no additional action required for return null 
        # Process fail_row behaviour. 
        if found_none_behaviour == "fail_row":

            condition_expr = None
            if conditions:
                for condition in conditions:
                    column = condition["column"]
                    comparison = condition["comparison"]
                    value = condition["value"]

                    if comparison == "eq":
                        expr = F.col(column) == value
                    elif comparison == "ne":
                        expr = ((F.col(column) != value) | (F.col(column).isNull()) )
                    else:
                        if self.verbose_logging:
                            self.logger.warning(f"Unsupported comparison operator: {comparison} in {rule_name}")

                    if condition_expr is None:
                        condition_expr = expr
                    else:
                        condition_expr = condition_expr & expr
            
            # Only apply the condition if it contains a value other than None
            if validate_null:
                if condition_expr is not None:
                    errors_df = matched_df.where(check_match_columns_expr & condition_expr)
                else:
                    errors_df = matched_df.where(check_match_columns_expr)
            else:
                if condition_expr is not None:
                    errors_df = matched_df.where((check_match_columns_expr & F.col(source_col).isNotNull()) & condition_expr)
                else:
                    errors_df = matched_df.where(check_match_columns_expr & F.col(source_col).isNotNull())

            errors_df = errors_df.withColumn("error_message", F.lit(no_match_entity_error))

            self._log_failed_rows(errors_df, validation, rule_name, "matching")

        duplicates_df = matched_df.groupBy("row_id").count().where(F.col("count") > 1)
    
        if duplicates_df.count() > 0:
            if found_multiple_behaviour == "oldest" or found_multiple_behaviour == "any":
                matched_df = (
                    matched_df
                    .withColumn("row_num", F.row_number().over(
                        W.partitionBy("row_id").orderBy(F.col("createdon").asc())
                    ))
                )
            elif found_multiple_behaviour == "newest":
                matched_df = (
                    matched_df
                    .withColumn("row_num", F.row_number().over(
                        W.partitionBy("row_id").orderBy(F.col("createdon").desc())
                    ))
                )
            else:  
                #failrow. Keep the newest to prevent duplicates in onward processing, but include an error
                matched_df = (
                    matched_df
                    .withColumn("row_num", F.row_number().over(
                        W.partitionBy("row_id").orderBy(F.col("createdon").desc())
                    ))
                )
                # Get one error per row_id
                errors_df = matched_df.where("row_num == 2")
                errors_df = errors_df.withColumn("error_message", F.lit(multiple_match_entity_error))
                for row in errors_df.collect():
                    self._log_failed_rows(errors_df, validation, rule_name, "matching")
                        
            # Dedupe just selecting the oldest, newest, or any row as required
            matched_df = matched_df.where("row_num == 1").drop("row_num")

        matched_df = matched_df.drop("createdon")


        return matched_df
        
    def _match_to_external_reference(self, source_data_df: DataFrame, data_source_column: str,data_source_detail: str, target_entity: str, output_column: str, 
                                ext_reference_column: str, behaviour:str, error_message: str, rule_name:str) -> DataFrame:
        """Function to match a given data_source_column to an external reference table.

        Args:
            source_data_df (DataFrame) : Spark dataframe containing source data
            data_source_column (str) : The column in the source data containing the ID of the Data Source.
            data_source_detail (str) : A string value for the column name of field name of how the Source data refers to this unique ID. Does not actually refer to a column in the source data.
            target_entity (str) : (If given) The logical name of the expected entity that this ID should look up to.
            environment (str) : Current environment. Must be : dev or prod or preprod or test
            output_column (str): The name of the matched GUID should be output to.
            ext_reference_column (str) : The column in the source data containing the ID field to look up.
            behaviour (str) : Optional behaviour that defines how this function should work.
            custom_error (str) : Error message to be written out.
            rule_name (str): Name of the metadata rule that called this function

        Returns:
            match_source_data_df (DataFrame): Transformed dataframe with the additional column.

        """
        
        if behaviour:
            behaviour = behaviour["found_none_behaviour"]
        else:
            behaviour = 'fail_row'
        
        validation = "Match to External Reference"
        ext_ref_error_message = error_message if error_message else "incorrect error message"
        #f"No matching External Reference for an active record can be found with data source: {data_source_column}, data source detail: {data_source_detail} and external reference: py3_externalreference. Create one or alter the information in those columns to address the error."

        # Read py3_externalreference into a dataframe, 
        # retrieving just the rows and columns required 
        # based on the data_source_column, data_source_detail, and ext_reference_column, 
        # and target_entity if supplied
        filter_condition = (
            f"LOWER(shl_datasourcedetail) == '{data_source_detail.lower()}' AND LOWER(regardingobjectid_entitytype) == '{target_entity.lower()}'"
            if target_entity
            else f"LOWER(shl_datasourcedetail) == '{data_source_detail.lower()}'"
        )

        py3_ext_reference_df = (
            self._spark.table(f"{self.environment}_py3_externalreference")
            .select("py3_externalreference", "regardingobjectid", "regardingobjectid_entitytype", "shl_datasource", "shl_datasourcedetail", "py3_externalreference")
            .where(filter_condition)
        )

        # Join the spark data frame with the source data on the data_source_column, data_source_detail, and ext_reference_column values to get the regardingobjectid_entity column
        join_condition = (
            (F.lower(F.col("ext.shl_datasource")) == F.lower(F.col(f"src.{data_source_column}"))) &
            (F.lower(F.col("ext.shl_datasourcedetail")) == F.lower(F.lit(data_source_detail))) &
            (F.lower(F.col("ext.py3_externalreference")) == F.lower(F.col(f"src.{ext_reference_column}")))
        )

        extref_df = (
            source_data_df
            .alias("src")
            .join(py3_ext_reference_df.alias("ext"), join_condition, how="left")
        )

        # Extract distinct table names from the regardingobjectid_entitytype column
        table_names_df = extref_df.select("regardingobjectid_entitytype").distinct()
        table_names = [row["regardingobjectid_entitytype"] for row in table_names_df.collect()]

        # Iterate over each table name and perform the join
        for table_name in table_names:
            
            if table_name:
                # Load the table based on the table name
                entity_df = self._spark.table(f"{self.environment}_{table_name}").select("Id", "statecode")

                # Perform the join
                extref_df = (
                    extref_df
                    .alias("match")
                    .join(entity_df.alias("ent"), 
                        (F.col("match.regardingobjectid") == F.col("ent.Id")) & 
                        (F.col("ent.statecode") == 0), 
                        how="left")
                    .drop("statecode")
                )
        extref_df = extref_df.withColumn(f"{output_column}", F.col("Id")).drop("Id")

        
        if behaviour == 'fail_row':
            errors_df = extref_df.where(F.col(f"{output_column}").isNull())
            errors_df = errors_df.withColumn("error_message", F.lit(ext_ref_error_message))
            self._log_failed_rows(errors_df, validation, rule_name, "matching", ext_ref_error_message)
        
        # Drop other unused columns
        columns_to_drop = ["shl_datasource","shl_datasourcedetail","py3_externalreference","regardingobjectid","regardingobjectid_entitytype"]
        extref_df = extref_df.drop(*columns_to_drop)

        return extref_df
    

    def _match_to_type(self, source_data_df: DataFrame, entity:str, column:str, output:str, parent:str, group: str, conditions:list[dict], error_message: str, rule_name:str) -> DataFrame:
        """ Matches rows the entity CRM table using parent or group. 
            Configures match_filter and output_columns List[Dict] and behaviour Dict based on incoming metadata
            Then calls match_to_entity

        Args:
            source_data_df (DataFrame) : Spark dataframe containing source data
            entity (str): the name of the table in CRM to lookup against
            column (str): The column to filter by joined on source (e.g. Title)
            output (str): The output column to write the match to
            parent (str): The guid to filter by
            group  (str): The guid to filter by
            conditions:list[dict]: Conditions under which the value is to be assigned for the row
            error_message (str): Custom error if supplied
            rule_name (str): Name of the metadata rule that called this function

        Returns
            match_source_data_df (DataFrame): Transformed dataframe with the additional column.
        """
        if parent:
            match_filters = [{"filter_on":"py3_parenttypeid","filter_by_value":parent},{"filter_on":"py3_name", "filter_by_column":column}]
        elif group:
            match_filters = [{"filter_on":"py3_optionsetgroupid","filter_by_value":group},{"filter_on":"py3_name", "filter_by_column":column}]

        behaviour = {"found_none_behaviour":"fail_row","found_multiple_behaviour":"any"}
        output_columns = [{"column_name_in_scrm":"py3_typeid","output":output}]

        matched_df = self._match_to_entity(source_data_df=source_data_df,
                                           entity=entity,
                                           match_filters=match_filters,
                                           behaviour=behaviour,
                                           output_columns=output_columns,
                                           validate_null=False,
                                           conditions=conditions,
                                           custom_error=error_message,
                                           validation="Match to Type",
                                           rule_name=rule_name)
        

        return matched_df