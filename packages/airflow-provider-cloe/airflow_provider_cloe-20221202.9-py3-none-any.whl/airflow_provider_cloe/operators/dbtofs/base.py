from airflow.models import BaseOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow_provider_cloe.utils.templating_engine import env_sql


class DBToFS(BaseOperator):
    def __init__(
        self,
        *args,
        source_conn_id: str,
        source_selectstatement: str,
        sink_conn_id: str,
        sink_container_name: str,
        sink_folder_path: str,
        sink_file_name: str,
        sink_file_format: str,
        datasourceinfo_id: str,
        datasettype_id: str,
        filecatalog_conn_id: str,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.source_conn_id = source_conn_id
        self.source_selectstatement = source_selectstatement
        self.sink_conn_id = sink_conn_id
        self.sink_container_name = sink_container_name
        self.sink_folder_path = sink_folder_path
        self.sink_file_name = sink_file_name
        self.sink_file_format = sink_file_format
        self.datasourceinfo_id = datasourceinfo_id
        self.datasettype_id = datasettype_id
        self.filecatalog_conn_id = filecatalog_conn_id

    def insert_into_filecatalog(self, sink_files: list[dict]) -> None:
        self.log.info(
            "Retrieving connection file catalog %s...", self.filecatalog_conn_id
        )
        odbc_hook = SnowflakeHook(snowflake_conn_id=self.filecatalog_conn_id)
        if len(sink_files) > 0:
            self.log.info("Inserting file into filecatalog...")
            query_file_insert = env_sql.get_template(
                "filecatalog_insert_files.sql.j2"
            ).render(
                sink_folder_path=self.sink_folder_path,
                sink_file_names=sink_files,
                file_status=0,
                datasourceinfo_id=self.datasourceinfo_id,
                datasettype_id=self.datasettype_id,
                sink_conn_id=self.sink_conn_id,
            )
            odbc_hook.run(query_file_insert)
            self.log.info("...Success!")
        else:
            self.log.info("No files written, not inserting.")
