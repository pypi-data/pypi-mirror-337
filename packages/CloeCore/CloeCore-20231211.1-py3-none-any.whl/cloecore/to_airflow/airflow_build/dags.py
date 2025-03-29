import logging
import uuid

import cloecore.utils.model as meta
from cloecore.to_airflow.airflow_build import tasks
from cloecore.to_airflow.model.dag import DAG

logger = logging.getLogger(__name__)


def create_dags(
    batches: list[meta.Batch],
    jobs: dict[uuid.UUID, meta.DB2FS | meta.FS2DB | meta.ExecSQLJob],
    connections: dict[uuid.UUID, meta.Connection],
) -> list[DAG]:

    dags = []
    for n, batch in enumerate(batches):
        dag_name = f"Batch_{n}"
        dag_tasks = tasks.batchsteps_to_tasks(batch.batchsteps, jobs, connections)
        dag = DAG(dag_name, batch.cron, dag_tasks)
        dags.append(dag)
    return dags
