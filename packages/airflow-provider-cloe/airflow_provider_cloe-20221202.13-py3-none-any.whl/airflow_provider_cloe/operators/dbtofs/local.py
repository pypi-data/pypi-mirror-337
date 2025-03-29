import os
import tempfile

from airflow.hooks.dbapi import DbApiHook
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow_provider_cloe.operators.dbtofs.base import DBToFS
from airflow_provider_cloe.utils.templating_engine import env_sql


class LocalDBToFS(DBToFS):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def load_data_from_db(self, hook: DbApiHook) -> None:
        self.log.info("Loading data from db...")
        self.df = hook.get_pandas_df(sql=self.source_selectstatement)
        self.log.info("Loading data from db...Success!")

    def load_data_into_blob(self, file_name: str, whook: WasbHook) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            to_delete_name = temp_file.name
            self.log.info("Saving data on disk...")
            self.df.to_parquet(
                temp_file.name, compression="snappy", engine="pyarrow", index=False
            )
            self.log.info("Saving data on disk...Success!")
            self.log.info("Uploading file from disk to Blob...")
            whook.load_file(
                file_path=temp_file.name,
                container_name=self.sink_container_name,
                blob_name=f"{self.sink_folder_path}/{file_name}",
            )
            self.log.info("Uploading file from disk to Blob...Success!")
        os.remove(to_delete_name)
