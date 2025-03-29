import datetime

from cloecore.to_airflow.model import tasks
from cloecore.to_airflow.templating_engine import env_air


class DAG:
    """
    Base class resembles a Airflow DAG.
    """

    def __init__(
        self,
        name: str,
        cron_schedule: str,
        tasks: list[
            tasks.SnowflakeFS2DBTask
            | tasks.SnowflakeExecutorTask
            | tasks.ODBCDB2FSTask
            | tasks.ODBCFS2DBTask
        ],
    ) -> None:
        self.id = name
        self.dag_owner = "airflow"
        self.schedule_interval = cron_schedule
        self.tasks = tasks
        self.tags = ["cloe"]

    def to_python(self) -> str:
        libraries_part = {task.to_python_libraries() for task in self.tasks}
        task_part = [task.to_python() for task in self.tasks]
        dep_part = []
        for task in self.tasks:
            dep_part += task.to_dependencies()
        dag_start_time = datetime.date.today().strftime("%Y-%m-%d")
        template = env_air.get_template("airflow_dag.py.j2")
        dag_string = template.render(
            libraries=libraries_part,
            dag_name=self.id,
            dag_owner=self.dag_owner,
            dag_cron=self.schedule_interval,
            dag_start_date=dag_start_time,
            tags=self.tags,
            tasks=task_part,
            dependencies=dep_part,
        )
        return dag_string
