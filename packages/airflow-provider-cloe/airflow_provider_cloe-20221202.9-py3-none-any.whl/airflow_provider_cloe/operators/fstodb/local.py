import os
import tempfile

import pandas as pd
from airflow.hooks.dbapi import DbApiHook
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow_provider_cloe.operators.fstodb.base import FSToDB
from airflow_provider_cloe.utils.templating_engine import env_sql


class LocalFSToDB(FSToDB):
    def __init__(
        self,
        *args,
        source_container_name: str,
        datasourceinfo_id: str = None,
        datasettype_id: str = None,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.source_container_name = source_container_name
        self.datasourceinfo_id = datasourceinfo_id
        self.datasettype_id = datasettype_id

    def load_parquet_from_blob(self, file_name: str, whook: WasbHook) -> None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                to_delete_name = temp_file.name
                self.log.info("Downloading data from blob: %s", file_name)
                whook.get_file(
                    file_path=temp_file.name,
                    container_name=self.source_container_name,
                    blob_name=file_name,
                )
                self.log.info("Loading file from disk...")
                self.file_df = pd.read_parquet(temp_file.name)
                self.log.info("Loading file from disk...Success!")
        finally:
            os.remove(to_delete_name)

    def load_data_into_db(self, hook: DbApiHook) -> None:
        self.log.info("Loading file into db...")
        self.file_df["insert_values"] = self.file_df.apply(
            lambda row: "('" + "','".join([str(i) for i in row]) + "')", axis=1
        )
        insert_df = (
            self.file_df[["insert_values"]]
            .assign(insert_group=(self.file_df.index / 1000).astype(int))
            .groupby("insert_group")
            .agg(lambda column: ",".join(column))
        )
        insert_columns = ",".join(list(self.file_df.columns[:-1]))
        insert_template = env_sql.get_template("table_insert_into.sql.j2")
        for index, row in insert_df.iterrows():
            self.log.debug("Group %s - Inserting values...", index)
            insert_query = insert_template.render(
                sink_table=self.sink_table,
                insert_columns=insert_columns,
                insert_values=row["insert_values"],
            )
            hook.run(insert_query)
        self.log.info("...Success!")
