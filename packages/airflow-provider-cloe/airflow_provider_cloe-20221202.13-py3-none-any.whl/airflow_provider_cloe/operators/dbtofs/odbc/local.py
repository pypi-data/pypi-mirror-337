from datetime import datetime
from typing import Any, Optional

import adlfs
import pyarrow.parquet as pq
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.odbc.hooks.odbc import OdbcHook
from airflow_provider_cloe.operators.dbtofs.local import LocalDBToFS
from turbodbc import Rows, connect, make_options
from turbodbc.connection import Connection


class DBToFSOdbcLocalOperator(LocalDBToFS):
    def get_turbodbc_connection(
        self, odbc_hook: OdbcHook, turbodbc_options: Optional[dict] = None
    ) -> Connection:
        default_options_kwargs = dict(
            read_buffer_size=Rows(100000),
            large_decimals_as_64_bit_types=True,
            parameter_sets_to_buffer=1000,
            prefer_unicode=True,
            autocommit=True,
        )
        turbodbc_options = make_options(
            **{**default_options_kwargs, **(turbodbc_options or {})}
        )
        self.log.info("Turbodbc options set. Testing connection...")
        return connect(
            connection_string=odbc_hook.odbc_connection_string,
            turbodbc_options=turbodbc_options,
        )

    def load_data_batches_into_blob(
        self, file_name: str, odbc_hook: OdbcHook, whook: WasbHook
    ) -> list[dict]:
        blob_conn = whook.get_conn()
        files_wrote = []
        acc_name = blob_conn.primary_hostname.split(".")[0]
        self.log.info(
            "Extracted '%s' as Azure Storage Account name from connection string. Checking connection...",
            acc_name,
        )
        blob_fs = adlfs.AzureBlobFileSystem(
            account_name=acc_name, credential=blob_conn.credential
        )
        connection = self.get_turbodbc_connection(odbc_hook)
        cursor = connection.cursor()
        self.log.info("Executing Query...")
        cursor.execute(self.source_selectstatement)
        batches = cursor.fetachallarrow()
        ctx = None
        iter_filename = file_name.replace(".parquet", "")
        self.log.info("Using '%s' as iterator filename...", iter_filename)
        for ctx, batch in enumerate(batches):
            wrote_files = True
            self.log.info("Transforming numpy batch %s into pyarrow table...", ctx)
            part_filename = f"{self.sink_container_name}/{self.sink_folder_path}/{iter_filename}/part_{ctx}.parquet"
            self.log.info("Uploading to %s...", part_filename)
            pq.write_table(batch, part_filename, filesystem=blob_fs)
        if wrote_files:
            files_wrote = [
                {
                    "sink_folder_path": self.sink_folder_path,
                    "sink_file_name": iter_filename,
                    "sink_file_parts": (ctx or 0) + 1,
                }
            ]
        else:
            self.log.warning("No batches or empty resultset.")
        self.log.info("All complete, closing connection...")
        cursor.close()
        connection.close()
        return files_wrote

    def execute(self, context: Any) -> None:
        self.log.info("Retrieving connection source %s...", self.source_conn_id)
        odbc_hook = OdbcHook(odbc_conn_id=self.source_conn_id)
        self.log.info("Retrieving connection sink %s...", self.sink_conn_id)
        azure_hook = WasbHook(wasb_conn_id=self.sink_conn_id)
        file_name_with_ts = f"{self.sink_file_name}.{datetime.now().strftime('%Y%m%d%H%M%S')}.{self.sink_file_format}"
        files_wrote = self.load_data_batches_into_blob(
            file_name_with_ts, odbc_hook=odbc_hook, whook=azure_hook
        )
        self.insert_into_filecatalog(files_wrote)
