import logging

import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def create_batch(model_batches: list[meta.Batch]) -> tuple[list, list, list]:
    batch_id = 0
    batchstep_id = 0
    batches = []
    batchsteps = []
    batchstep_dependencies = []
    for batch in model_batches:
        batch_id += 1
        batchstep_dep = {
            batchstep.id: batchstep.get_dependencies() for batchstep in batch.batchsteps
        }
        batch_lite = BatchRefresh(batch.name, batch_id, batch.tags)
        batchstep_execute_id, batchstep_local, deps = Batchstep(
            batch_id, batch.batchsteps, batchstep_dep, batchstep_id
        )
        batchsteps += batchstep_local
        batchstep_dependencies += deps
        batchstep_id = batchstep_execute_id

        batches.append(batch_lite)
        logger.info("Batch %s created", batch_id)

    return batches, batchsteps, batchstep_dependencies


def BatchRefresh(batch_name: str, batch_id: int, batch_tags: str | None = None) -> dict:
    """Transforms a regular batch to a sql-orchestrator batch
    with auto refresh.

    Args:
        batch_name (str): _description_
        batch_id (int): _description_
        batch_tags (str): _description_

    Returns:
        dict: _description_
    """
    batch = {}
    batch["type"] = "Refresh"
    batch["status"] = str(10)
    batch["is_active"] = str(1)
    batch["name"] = batch_name
    batch["id"] = str(batch_id)
    if batch_tags is not None:
        batch["tags"] = batch_tags

    return batch


def Batchstep(
    batch_id: int,
    batchsteps: list[meta.Batchstep],
    batchstep_dep: dict,
    batchstep_execute_id: int,
) -> tuple[int, list, list]:
    batchstep_local = []
    batchstep_trans = {}
    batchstep_base = {}
    batchstep_base["fk_batch_id"] = batch_id
    batchstep_base["status"] = 10
    batchstep_base["is_active"] = 1
    for batchstep in batchsteps:
        batchstep_execute_id += 1
        current_batchstep: dict[str, str | int] = dict(batchstep_base)
        current_batchstep["id"] = batchstep_execute_id
        current_batchstep["fk_job_id"] = str(batchstep.job_id)
        if batchstep.tags is not None:
            current_batchstep["tags"] = batchstep.tags
        batchstep_local.append(current_batchstep)
        batchstep_trans[batchstep.id] = batchstep_execute_id
    deps = BatchstepDependencies(batchstep_trans, batchstep_dep)

    return batchstep_execute_id, batchstep_local, deps


def BatchstepDependencies(batchstep: dict, batchstep_dep: dict) -> list:
    deps = []
    for real_id, exec_id in batchstep.items():
        for dep in batchstep_dep[real_id]:
            current_entry = {}
            current_entry["fk_batchstep_id"] = exec_id
            current_entry["fk_batchstep_dependency_id"] = batchstep[dep]
            deps.append(current_entry)
    return deps
