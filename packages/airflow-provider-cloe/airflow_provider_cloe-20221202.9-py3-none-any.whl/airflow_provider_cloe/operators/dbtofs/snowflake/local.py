from datetime import datetime
from typing import Any

from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow_provider_cloe.operators.dbtofs.local import LocalDBToFS


class DBToFSSnowflakeLocalOperator(LocalDBToFS):
    def execute(self, context: Any) -> None:
        snowflake_hook = SnowflakeHook(conn_name_attr=self.sink_conn_id)
        azure_hook = WasbHook(wasb_conn_id=self.source_conn_id)
        file_name_with_ts = f"{self.sink_file_name}.{datetime.now().strftime('%Y%m%d%H%M%S')}.{self.sink_file_format}"
        self.load_data_from_db(snowflake_hook)
        self.load_data_into_blob(file_name_with_ts, azure_hook)
        self.call_postload_procedure(snowflake_hook)
        self.insert_into_filecatalog(
            [
                {
                    "sink_folder_path": self.sink_folder_path,
                    "sink_file_name": file_name_with_ts,
                    "sink_file_parts": 1,
                }
            ]
        )
