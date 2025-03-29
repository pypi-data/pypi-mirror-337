import json
from typing import Any, Optional

import pandas as pd
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow_provider_cloe.operators.fstodb.base import FSToDB
from airflow_provider_cloe.utils.templating_engine.sql_templates import env_sql
from snowflake.connector import ProgrammingError


class FSToDBSnowflakeRemoteOperator(FSToDB):
    """Class is implementing the standard filestorage to
    database workflow for remote operations.

    Args:
        FSToDB (_type_): _description_
    """

    def __init__(self, *args, stage_name: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stage_name = stage_name
        self.table_truncate_template_filename = "table_truncate.sql.j2"

    def copy_into_table_direct(self, file: str, shook: SnowflakeHook) -> None:
        """Loads simple structure like csv data from stage into stage table.

        Args:
            file (str): _description_
            shook (SnowflakeHook): _description_
        """
        self.log.info("Truncating table sink table %s...", self.sink_table)
        truncate_query = env_sql.get_template(
            self.table_truncate_template_filename
        ).render(sink_table=self.sink_table)
        shook.run(truncate_query, True)
        self.log.info("Executing COPY into %s...", self.sink_table)
        copy_into_query = env_sql.get_template("table_copy_into.sql.j2").render(
            sink_table=self.sink_table,
            stage_name=self.stage_name,
            file=file,
            source_file_format=self.source_file_format,
        )
        shook.run(copy_into_query, True)
        self.log.info("Updating ETL columns in %s...", self.sink_table)
        update_query = env_sql.get_template("update_stage_filename.sql.j2").render(
            sink_table=self.sink_table, source_file_name=file
        )
        shook.run(update_query, True)
        self.log.info("COPY command completed.")

    @staticmethod
    def match_raw_and_stage_table_names(
        raw_table_name: str, stage_table_name: str, shook: SnowflakeHook
    ) -> list:
        """Matches raw and stage table columns by normalizing them.

        Args:
            raw_table_name (str): _description_
            stage_table_name (str): _description_

        Returns:
            list: a list of dicts with matching columns
        """
        raw_query = f"select content from {raw_table_name} limit 1;"
        stage_query = f"DESCRIBE TABLE {stage_table_name};"
        raw_result = shook.get_records(raw_query)
        stage_result = shook.get_records(stage_query)
        raw_colums = json.loads(raw_result[0][0])
        raw_colums_normalized = {i.lower(): i for i in raw_colums.keys()}
        mapping = []
        for row in stage_result:
            normalized_col_name = row[0].lower()
            if normalized_col_name in raw_colums_normalized:
                mapping.append(
                    {
                        "raw_col_name": raw_colums_normalized[normalized_col_name],
                        "stage_col_name": row[0],
                    }
                )
        return mapping

    def copy_into_table_raw(
        self,
        file_path_full: str,
        shook: SnowflakeHook,
        multi_file: Optional[bool] = False,
    ) -> None:
        """Function loads more complex data structures like parquet
        or avros. It first loads the data into a intermediate table and
        then to a stage table.

        Args:
            file_path_full (str): _description_
            shook (SnowflakeHook): _description_
            multi_file (Optional[bool], optional): _description_. Defaults to False.
        """
        raw_table_name = f"{self.sink_table}_raw"
        self.log.info("Truncating table raw sink table %s...", raw_table_name)
        truncate_query = env_sql.get_template(
            self.table_truncate_template_filename
        ).render(sink_table=raw_table_name)
        shook.run(truncate_query, True)
        self.log.info("Executing COPY into %s...", raw_table_name)
        use_pattern = multi_file
        copy_into_query = env_sql.get_template("table_copy_into.sql.j2").render(
            sink_table=raw_table_name,
            stage_name=self.stage_name,
            use_pattern=use_pattern,
            file_path_full=file_path_full,
            source_file_format=self.source_file_format,
        )
        shook.run(copy_into_query, True)
        self.log.info("COPY command completed.")
        self.log.info("Retrieving stage and raw table information...")
        mapping = self.match_raw_and_stage_table_names(
            raw_table_name=f"{self.sink_table}_raw",
            stage_table_name=self.sink_table,
            shook=shook,
        )
        self.log.info("Truncating table stage sink table %s...", self.sink_table)
        truncate_query = env_sql.get_template(
            self.table_truncate_template_filename
        ).render(sink_table=self.sink_table)
        shook.run(truncate_query, True)
        self.log.info("Executing semi structured INSERT command...")
        insert_into_query = env_sql.get_template(
            "snowflake_insert_into_from_raw.sql.j2"
        ).render(
            sink_table=self.sink_table,
            sink_columns=[col["stage_col_name"] for col in mapping],
            raw_columns=[col["raw_col_name"] for col in mapping],
            source_table=raw_table_name,
        )
        shook.run(insert_into_query, True)
        self.log.info("COPY command completed.")
        self.log.info("Updating ETL columns in %s...", self.sink_table)
        update_query = env_sql.get_template("update_stage_filename.sql.j2").render(
            sink_table=self.sink_table, source_file_name=file_path_full
        )
        shook.run(update_query, True)

    def get_new_files_from_stage(
        self, processed_files: pd.DataFrame, shook: SnowflakeHook
    ) -> list:
        """Gets files from snowflake stage based on defined pattern.
        Retrieved files are cleaned - url is removed using stage describe.

        Args:
            processed_files (pd.DataFrame): _description_
            shook (SnowflakeHook): _description_

        Returns:
            list: _description_
        """
        fp_pattern = f"{self.source_file_path_pattern.replace('%', '.*')}{self.source_file_name_pattern.replace('%', '.*')}"
        self.log.info("Requesting stage files, using pattern %s...", fp_pattern)
        query_get_files = env_sql.get_template("stage_list.sql.j2").render(
            stage_name=self.stage_name, pattern=fp_pattern
        )
        list_describe = env_sql.get_template("stage_describe.sql.j2").render(
            stage_name=self.stage_name
        )
        self.log.info("Retrieving stage information and cleaning url...")
        list_describe_result_set = shook.get_pandas_df(list_describe)
        list_describe_result_set.columns = list_describe_result_set.columns.str.lower()
        url = list_describe_result_set[
            list_describe_result_set.property == "URL"
        ].property_value.values[0]
        replace_parts = {'"': "", "[": "", "]": ""}
        for k, v in replace_parts.items():
            url = url.replace(k, v)
        self.log.info(
            "Retrieving all files matching pattern from stage and cleaning name..."
        )
        result_set_files_in_blob = shook.get_pandas_df(query_get_files)
        result_set_files_in_blob.columns = result_set_files_in_blob.columns.str.lower()
        result_set_files_in_blob["last_modified"] = pd.to_datetime(
            result_set_files_in_blob["last_modified"], format="%a, %d %b %Y %H:%M:%S %Z"
        )
        result_set_files_in_blob["name"] = result_set_files_in_blob["name"].str.replace(
            url, ""
        )
        self.log.info("Removing processed files from stage file result set...")
        unprocessed_files = (
            result_set_files_in_blob.merge(
                processed_files, on=["name"], how="left", indicator=True
            )
            .query('_merge == "left_only"')
            .drop(columns="_merge")
        )
        return unprocessed_files.sort_values(by=["last_modified"], ascending=True)[
            "name"
        ].to_list()

    def process_files_from_stage(
        self, fc_snf_hook: SnowflakeHook, sink_snf_hook: SnowflakeHook
    ) -> None:
        """Retrieves files from stage based on defined pattern.
        Compares retrieved files to processed files in file catalog.
        Loads files not in file catalog.

        Args:
            fc_snf_hook (SnowflakeHook): _description_
            sink_snf_hook (SnowflakeHook): _description_

        Raises:
            e: _description_
        """
        processed_files = self.get_processed_files_from_filecatalog(fc_snf_hook)
        unprocessed_files = self.get_new_files_from_stage(processed_files, fc_snf_hook)
        if len(unprocessed_files) < 1:
            self.log.info("No unprocessed files matching defined pattern found.")
        else:
            for file in unprocessed_files:
                try:
                    if self.source_file_type.lower() in ("parquet", "avro"):
                        self.copy_into_table_raw(file, sink_snf_hook)
                    else:
                        self.copy_into_table_direct(file, sink_snf_hook)
                        self.call_postload_procedure(sink_snf_hook)
                        self.insert_into_filecatalog(file, fc_snf_hook)
                except ProgrammingError as error:
                    self.update_filecatalog(
                        file["id"], fc_snf_hook, failed=True, error_message=error.msg
                    )
                    raise error

    def process_files_from_file_catalog(
        self, fc_snf_hook: SnowflakeHook, sink_snf_hook: SnowflakeHook
    ) -> None:
        """Gets unprocessed files from file catalog and
        loads them to snowflake.

        Args:
            fc_snf_hook (SnowflakeHook): _description_
            sink_snf_hook (SnowflakeHook): _description_

        Raises:
            e: _description_
        """
        unprocessed_files = self.get_unprocessed_files_from_filecatalog(fc_snf_hook)
        for index, file in unprocessed_files.iterrows():
            try:
                if self.source_file_type.lower() in ("parquet", "avro"):
                    self.copy_into_table_raw(
                        f"{file['filepath']}/{file['filename']}", sink_snf_hook, True
                    )
                else:
                    self.copy_into_table_direct(
                        f"{file['filepath']}/{file['filename']}", sink_snf_hook
                    )
                self.call_postload_procedure(sink_snf_hook)
                self.update_filecatalog(file["id"], fc_snf_hook)
            except ProgrammingError as error:
                self.update_filecatalog(
                    file["id"], fc_snf_hook, failed=True, error_message=error.msg
                )
                raise error

    def execute(self, context: Any) -> None:
        sink_snf_hook = SnowflakeHook(snowflake_conn_id=self.sink_conn_id)
        fc_snf_hook = SnowflakeHook(snowflake_conn_id=self.filecatalog_conn_id)
        if not self.get_from_filecatalog:
            self.process_files_from_stage(
                fc_snf_hook=fc_snf_hook, sink_snf_hook=sink_snf_hook
            )
        else:
            self.process_files_from_file_catalog(
                fc_snf_hook=fc_snf_hook, sink_snf_hook=sink_snf_hook
            )
