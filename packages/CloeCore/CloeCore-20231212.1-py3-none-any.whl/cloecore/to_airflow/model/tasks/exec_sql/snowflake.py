import uuid

from cloecore.to_airflow.model.tasks import base


class SnowflakeExecutorTask(base.BaseTask):
    library: str = "airflow.providers.snowflake.operators.snowflake"
    imports: str = "SnowflakeOperator"

    def __init__(
        self,
        name: str,
        task_n: uuid.UUID,
        depends_on: list[uuid.UUID],
        sql_query: str,
        connection_id: uuid.UUID,
    ) -> None:
        super().__init__(name, task_n, depends_on)
        self.sql_query = sql_query
        self.connection_id = connection_id

    def to_python(self) -> str:
        return (
            f"t{str(self.task_n).replace('-', '')} = SnowflakeOperator(\n"
            f"task_id='{str(self.task_n).replace('-', '')}"
            f"_{self.task_name}',\nsnowflake_conn_id='{self.connection_id}',\n"
            f"sql='{self.sql_query}',\ndag=dagone)\n"
        )
