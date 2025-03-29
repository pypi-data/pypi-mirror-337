import uuid
from typing import Any, Optional

import pandas as pd
from airflow.hooks.dbapi import DbApiHook
from airflow.models import BaseOperator
from airflow_provider_cloe.utils.templating_engine import env_sql


class FSToDB(BaseOperator):
    """Base class for all FSToDB jobs.

    Args:
        BaseOperator (_type_): _description_
    """

    def __init__(
        self,
        *args,
        sink_table: str,
        sink_conn_id: str,
        get_from_filecatalog: bool,
        filecatalog_conn_id: str,
        source_conn_id: str,
        source_file_format: str,
        source_file_type: Optional[str] = "parquet",
        source_file_path_pattern: Optional[str] = "",
        source_file_name_pattern: Optional[str] = "",
        datasourceinfo_id: Optional[str] = None,
        datasettype_id: Optional[str] = None,
        postload_job_call_query: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.sink_table = sink_table
        self.source_file_format = source_file_format
        self.sink_conn_id = sink_conn_id
        self.filecatalog_conn_id = filecatalog_conn_id
        self.get_from_filecatalog = get_from_filecatalog
        self.source_conn_id = source_conn_id
        self.source_file_type = source_file_type
        self.source_file_path_pattern = source_file_path_pattern
        self.source_file_name_pattern = source_file_name_pattern
        self.datasourceinfo_id = datasourceinfo_id
        self.datasettype_id = datasettype_id
        self.postload_job_call_query = postload_job_call_query

    def get_unprocessed_files_from_filecatalog(self, hook: DbApiHook) -> pd.DataFrame:
        """Gets all files from file catalog that are marked with status <1.

        Args:
            hook (DbApiHook): _description_

        Returns:
            pd.DataFrame: _description_
        """
        file_lock_uuid = str(uuid.uuid1())
        self.log.info("Locking unprocessed files from filecatalog...")
        query_file_lock = env_sql.get_template(
            "filecatalog_update_files.sql.j2"
        ).render(
            file_status=1,
            file_lock_uuid=file_lock_uuid,
            source_file_path_pattern=self.source_file_path_pattern,
            source_file_name_pattern=self.source_file_name_pattern,
        )
        hook.run(query_file_lock)
        self.log.info("Getting locked files from filecatalog...")
        query_get_locked = env_sql.get_template(
            "filecatalog_select_files.sql.j2"
        ).render(file_status=1, file_lock_uuid=file_lock_uuid)
        unprocessed_files_result_set = hook.get_pandas_df(query_get_locked)
        unprocessed_files_result_set.columns = (
            unprocessed_files_result_set.columns.str.lower()
        )
        return unprocessed_files_result_set

    def get_processed_files_from_filecatalog(self, hook: DbApiHook) -> pd.DataFrame:
        """Gets all files from file catalog that are marked with status >1.

        Args:
            hook (DbApiHook): _description_

        Returns:
            pd.DataFrame: _description_
        """
        self.log.info("Getting processed files from filecatalog...")
        query_get_processed = env_sql.get_template(
            "filecatalog_select_files.sql.j2"
        ).render(
            file_status=3,
            source_file_path_pattern=self.source_file_path_pattern,
            source_file_name_pattern=self.source_file_name_pattern,
        )
        processed_files_result_set = hook.get_pandas_df(query_get_processed)
        processed_files_result_set.columns = (
            processed_files_result_set.columns.str.lower()
        )
        return processed_files_result_set

    def insert_into_filecatalog(self, file_qualifier: str, hook: DbApiHook) -> None:
        """Insert a filename into file catalog.

        Args:
            file_qualifier (str): _description_
            hook (DbApiHook): _description_
        """
        split_file_path = f"{'/'.join(file_qualifier.split('/')[:-1])}/"
        split_file_name = file_qualifier.split("/")[-1]
        self.log.info("Inserting file into filecatalog...")
        query_file_insert = env_sql.get_template(
            "filecatalog_insert_files.sql.j2"
        ).render(
            sink_file_names=[
                {
                    "sink_folder_path": split_file_path,
                    "sink_file_name": split_file_name,
                    "sink_file_parts": 1,
                }
            ],
            file_status=3,
            datasourceinfo_id=self.datasourceinfo_id,
            datasettype_id=self.datasettype_id,
            sink_conn_id=self.sink_conn_id,
        )
        hook.run(query_file_insert)
        self.log.info("...Success!")

    def update_filecatalog(
        self,
        file_id: str,
        hook: DbApiHook,
        failed: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Updates an entry in file catalog with success or
        failure and an error message.

        Args:
            file_id (str): _description_
            hook (DbApiHook): _description_
            failed (bool, optional): _description_. Defaults to False.
            error_message (Optional[str], optional): _description_. Defaults to None.
        """
        self.log.info("Updating filecatalog, file id: %s...", file_id)
        if failed:
            file_status = 2
        else:
            file_status = 3
        query_file_update = env_sql.get_template(
            "filecatalog_update_files.sql.j2"
        ).render(file_status=file_status, file_id=file_id, error_message=error_message)
        hook.run(query_file_update)

    def call_postload_procedure(self, hook: DbApiHook) -> None:
        """Calls defined procedure after loading data into stage table.

        Args:
            hook (DbApiHook): _description_
        """
        if self.postload_job_call_query:
            self.log.info("Running given query %s", self.postload_job_call_query)
            hook.run(self.postload_job_call_query)
        else:
            self.log.info("No query given for postload execution. Continuing...")

    def execute(self, context: Any):
        """Needs to be overriden.

        Args:
            context (Any): _description_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()
