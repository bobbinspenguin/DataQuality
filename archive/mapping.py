def data_mapping(self, source_data_df: DataFrame, mapping_metadata: dict) -> None:

        id_column = mapping_metadata.get("id_column")
        persisted_df = self._persist_data(source_data_df, id_column)

        self._output_mapped_data(prepared_df=persisted_df, metadata=mapping_metadata)

        return

def _persist_data(self, source_data_df: DataFrame, id_column: str) -> DataFrame:
    """Generates a unique row identifier for each row in the dataframe based on a hash of all columns except the id_column.
    The function creates a hash of all columns except the id_column to identify unique rows. It then generates a UUID for each unique row and joins this back to the original dataframe.
    The resulting dataframe contains a new column 'row_id' with the unique identifier for each row."""
    # create hash on all columns except id_column
    hash_columns = [col for col in source_data_df.columns if col != id_column]
    source_data_df = source_data_df.withColumn("row_hash", F.sha2(F.concat_ws("||", *[F.col(c).cast("string") for c in hash_columns]), 256))

    ids_df = (
        source_data_df
        .select("row_hash")
        .withColumn(id_column, F.expr("uuid()"))
    )

    # Persist only the small dataframe with the id column and the hash to optimize performance
    ids_df.persist()

    # join ids_df back on source_data_df on the row_hash column
    joined_df = source_data_df.join(ids_df.select(id_column, "row_hash", "row_id"), on=["row_hash"], how="inner").drop("row_hash")


    return joined_df

def _output_mapped_data(self, prepared_df: DataFrame, metadata: dict) -> None:
    """Maps the prepared dataframe to the output tables as defined in the metadata and writes them to CSV."""
    # Get all tables which should be written
    table_mapping = metadata.get("tables")

    # Filter the list to get only which have been processed as a part of the data mapping
    table_names = [table.get("name") for table in table_mapping]

    for table_name in table_names:
        # Get source to target column mapping
        current_table = [table for table in table_mapping if table.get("name", None) == table_name][0]
        all_columns = current_table.get("columns", None)
        
        # Convert column mapping ot PySpark select expression
        source_to_target_columns = [column for column in all_columns if "source" in column]
        output_columns = [F.col(column["source"]).alias(column["target"]) for column in source_to_target_columns]

                    # Get derived column names and fixed values
        derived_columns = [column for column in all_columns if "value" in column]

        # Convert columns to a dictionary to filter duplicates
        column_dict = {str(column): column for column in output_columns}
        
        # Convert columns back to list
        output_columns = list(column_dict.values())

        output_df = prepared_df.select(*output_columns)
        
        # Add derived columns with fixed values
        for column in derived_columns:
            column_value = column["value"]
            target_column_name = column["target"]

            output_df = output_df.withColumn(target_column_name, F.lit(column_value))
        
        behaviour_filters = [{"target": column["target"], "match_type": column["behaviour"]["match_type"]} for column in all_columns if "behaviour" in column]

        for filter in behaviour_filters:
            filter_column = filter.get("target")
            match_type = filter.get("match_type")

            # If the value of the filter column is not equal to the match type then set it to null
            #  so that it is not updated in SCRM
            output_df = (
                output_df.withColumn(
                    filter_column,
                    F.when(
                        F.col("match_type") == match_type, F.col(filter_column)
                    ).otherwise(F.lit(None))
                )
            )
        
        conditions = current_table.get("conditions", [])
        
        for condition in conditions:
            condition_col = condition.get("column", None)
            comparison = condition.get("comparison", None)
            conditional_value = condition.get("value", None)

            if comparison == "eq":
                output_df = output_df.where(F.col(condition_col) == conditional_value)
        
        if not output_df.isEmpty():
            print(f"Writing output for {table_name}")

            (
                output_df
                .drop("match_type")
                .coalesce(1)
                .write
                .option("header", "true")
                .csv(f"Files/{FEED_NAME}/staging/{PIPELINE_RUN_ID}/output/{table_name}")
            )


    return