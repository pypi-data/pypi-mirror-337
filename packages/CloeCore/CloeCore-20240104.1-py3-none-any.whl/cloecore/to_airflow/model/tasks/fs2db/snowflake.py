import uuid

from cloecore.to_airflow.model.tasks.fs2db import base
from cloecore.to_airflow.templating_engine import env_air


class SnowflakeFS2DBTask(base.BaseFS2DBTask):
    library: str = "airflow_provider_cloe.operators"
    imports: str = "FSToDBSnowflakeRemoteOperator"

    def __init__(
        self,
        name: str,
        task_n: uuid.UUID,
        depends_on: list[uuid.UUID],
        source_connections_id: uuid.UUID,
        get_from_filecatalog: bool,
        filecatalog_connections_id: uuid.UUID,
        source_file_path_pattern: str,
        source_file_name_pattern: str,
        source_file_format: str,
        dataset_type_id: uuid.UUID,
        sink_connections_id: uuid.UUID,
        sink_table: str,
        stage_name: str,
        postload_job_call_query: str | None,
    ) -> None:
        super().__init__(
            name,
            task_n,
            depends_on,
            source_connections_id,
            get_from_filecatalog,
            filecatalog_connections_id,
            source_file_path_pattern,
            source_file_name_pattern,
            source_file_format,
            dataset_type_id,
            sink_connections_id,
            sink_table,
            postload_job_call_query,
        )
        self.stage_name = stage_name

    def to_python(self) -> str:
        return env_air.get_template("task_fstodb.py.j2").render(
            task_n=str(self.task_n).replace("-", ""),
            task_id=self.task_name,
            task_internal_name=self.imports,
            stage_name=self.stage_name,
            get_from_filecatalog=self.get_from_filecatalog,
            filecatalog_connections_id=self.filecatalog_connections_id,
            source_connections_id=self.source_connections_id,
            source_file_path_pattern=self.source_file_path_pattern,
            source_file_name_pattern=self.source_file_name_pattern,
            source_file_format=self.source_file_format,
            datasource_info_id=self.datasource_info_id,
            dataset_type_id=self.dataset_type_id,
            sink_connections_id=self.sink_connections_id,
            sink_table=self.sink_table,
            postload_job_call_query=self.postload_job_call_query,
        )
