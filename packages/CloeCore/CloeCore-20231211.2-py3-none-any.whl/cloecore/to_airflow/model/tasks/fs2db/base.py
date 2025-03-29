import uuid

from cloecore.to_airflow.model.tasks import base


class BaseFS2DBTask(base.BaseTask):
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
        postload_job_call_query: str | None,
    ) -> None:
        super().__init__(name, task_n, depends_on)
        self.source_connections_id = source_connections_id
        self.get_from_filecatalog = get_from_filecatalog
        self.filecatalog_connections_id = filecatalog_connections_id
        self.source_file_path_pattern = source_file_path_pattern
        self.source_file_name_pattern = source_file_name_pattern
        self.source_file_format = source_file_format
        self.datasource_info_id = "None"
        self.dataset_type_id = dataset_type_id
        self.sink_connections_id = sink_connections_id
        self.sink_table = sink_table
        self.postload_job_call_query = postload_job_call_query
