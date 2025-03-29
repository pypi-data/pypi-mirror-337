from typing import Any

from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.providers.odbc.hooks.odbc import OdbcHook
from airflow_provider_cloe.operators.fstodb.local import LocalFSToDB


class FSToDBOdbcLocalOperator(LocalFSToDB):
    def execute(self, context: Any) -> None:
        self.log.info("Retrieving connection source %s...", self.source_conn_id)
        azure_hook = WasbHook(wasb_conn_id=self.source_conn_id)
        self.log.info(f"Retrieving connection sink %s...", self.sink_conn_id)
        odbc_hook = OdbcHook(odbc_conn_id=self.sink_conn_id)
        if not self.get_from_filecatalog:
            self.log.error(
                "Direct load without filecatalog as primary is not implemented."
            )
            raise NotImplementedError
        else:
            unprocessed_files = self.get_unprocessed_files_from_filecatalog(odbc_hook)
            for file in unprocessed_files:
                try:
                    self.load_parquet_from_blob(f"{file[1]}/{file[2]}", azure_hook)
                    self.load_data_into_db(odbc_hook)
                    self.call_postload_procedure(odbc_hook)
                    self.update_filecatalog(file[0], odbc_hook)
                except:
                    self.update_filecatalog(file[0], odbc_hook, failed=True)
