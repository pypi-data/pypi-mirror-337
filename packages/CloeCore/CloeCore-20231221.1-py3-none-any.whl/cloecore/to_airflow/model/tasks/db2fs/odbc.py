import uuid

from cloecore.to_airflow.model.tasks import base
from cloecore.to_airflow.templating_engine import env_air


class ODBCDB2FSTask(base.BaseTask):
    library: str = "airflow_provider_cloe.operators"
    imports: str = "DBToFSOdbcLocalOperator"

    def __init__(
        self,
        name: str,
        task_n: uuid.UUID,
        depends_on: list[uuid.UUID],
        source_connections_id: uuid.UUID,
        select_statement: str,
        container_name: str,
        folder_path: str,
        sink_file_name: str,
        sink_file_format: str,
        datasource_info_id: uuid.UUID,
        dataset_type_id: uuid.UUID,
        sink_connections_id: uuid.UUID,
        filecatalog_connections_id: uuid.UUID,
    ) -> None:
        super().__init__(name, task_n, depends_on)
        self.source_connections_id = source_connections_id
        self.select_statement = select_statement
        self.folder_path = folder_path
        self.sink_file_name = sink_file_name
        self.sink_file_format = sink_file_format
        self.datasource_info_id = datasource_info_id
        self.dataset_type_id = dataset_type_id
        self.container_name = container_name
        self.sink_connections_id = sink_connections_id
        self.filecatalog_connections_id = filecatalog_connections_id

    def to_python(self) -> str:
        return env_air.get_template("task_dbtofs.py.j2").render(
            task_n=str(self.task_n).replace("-", ""),
            task_id=self.task_name,
            task_internal_name=self.imports,
            filecatalog_connections_id=self.filecatalog_connections_id,
            source_connections_id=self.source_connections_id,
            select_statement=self.select_statement,
            sink_connections_id=self.sink_connections_id,
            container_name=self.container_name,
            folder_path=self.folder_path,
            sink_file_name=self.sink_file_name,
            sink_file_format=self.sink_file_format,
            datasource_info_id=self.datasource_info_id,
            dataset_type_id=self.dataset_type_id,
        )
