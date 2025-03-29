import logging
import uuid

import cloecore.utils.model as meta
from cloecore.to_datafactory import packages

logger = logging.getLogger(__name__)


def distribute_batchsteps(
    dep_group_to_len: dict[str, int]
) -> dict[int, list[uuid.UUID]]:
    pipeline_length_max = 40
    pipelines: dict[int, list[uuid.UUID]] = {}
    pipeline_count = 0
    while len(dep_group_to_len) != 0:
        pipeline_length = 0
        pipeline_count += 1
        pipelines[pipeline_count] = []
        group_removal = []
        for k, v in sorted(dep_group_to_len.items(), reverse=True):
            if v > 40:
                logger.error(
                    (
                        "Batchstep dependency group %s is too long. Please split"
                        " manually or remove dependencies."
                    ),
                    k,
                )
                raise SystemExit("Batchstep dependency too long")
            if v + pipeline_length <= pipeline_length_max:
                pipeline_length += v
                pipelines[pipeline_count] += [uuid.UUID(i) for i in k.split(",")]
                group_removal.append(k)
        for k in group_removal:
            del dep_group_to_len[k]
    return pipelines


def calculate_length_of_dependency_groups(
    dependency_groups: list[list[int]], batchstep_to_length: dict
) -> dict[str, int]:
    dep_group_to_len: dict[str, int] = {}
    for dep_group in dependency_groups:
        dep_group_len = 0
        for batchstep in dep_group:
            dep_group_len += batchstep_to_length[batchstep]
        dep_group_to_len[",".join(str(i) for i in dep_group)] = dep_group_len
    return dep_group_to_len


def get_all_dependencies_of_leader(
    batchstep_id: int, batchstep_dependency_of: dict, batchstep_dependency_on: dict
) -> list[int]:
    dependency_group = [batchstep_id]
    current_deps = batchstep_dependency_of[batchstep_id]
    while True:
        current_deps_new = []
        for i in current_deps:
            if i in batchstep_dependency_of:
                current_deps_new += batchstep_dependency_of[i]
            if i in batchstep_dependency_on:
                current_deps_new += batchstep_dependency_on[i]
        dependency_group += current_deps
        current_deps = list(set(current_deps_new) - set(dependency_group))
        if len(current_deps_new) < 1:
            break
    logger.debug(
        "New dependency group found! It consists of %s.",
        ", ".join(str(i) for i in dependency_group),
    )
    return dependency_group


def get_dependency_groups_of_independent_bs(
    ind_batchsteps: list[int],
    batchstep_dependency_on: dict,
    batchstep_dependency_of: dict,
) -> list[list[int]]:
    batchsteps_loners = [
        [i] for i in ind_batchsteps if i not in batchstep_dependency_of
    ]
    batchsteps_leaders = list(
        set(ind_batchsteps) - set([i[0] for i in batchsteps_loners])
    )
    dependency_groups = []
    while len(batchsteps_leaders) > 0:
        dep_group = get_all_dependencies_of_leader(
            batchsteps_leaders[0], batchstep_dependency_of, batchstep_dependency_on
        )
        batchsteps_leaders = list(set(batchsteps_leaders) - set(dep_group))
        dependency_groups.append(dep_group)
    return dependency_groups + batchsteps_loners


def get_all_independent_batchsteps(
    batchsteps: list[int], batchstep_dependency_on: dict
) -> list[int]:
    return [i for i in batchsteps if i not in batchstep_dependency_on]


def transform_batchstep_deps(batchstep_dependency: dict) -> tuple[dict, dict]:
    batchstep_dependency_on = {}
    batchstep_dependency_of = {}
    for batchstep_id, step_dependencies in batchstep_dependency.items():
        if len(step_dependencies) > 0:
            batchstep_dependency_on[batchstep_id] = step_dependencies
            for dependency in step_dependencies:
                if dependency not in batchstep_dependency_of:
                    batchstep_dependency_of[dependency] = [batchstep_id]
                else:
                    batchstep_dependency_of[dependency].append(batchstep_id)
    return batchstep_dependency_on, batchstep_dependency_of


def create_dependency(obj_batchsteps: list[meta.Batchstep]) -> tuple[list, dict]:
    batchstep_dependency = {}
    batchsteps = []
    for batchstep in obj_batchsteps:
        batchsteps.append(batchstep.id)
        batchstep_dependency[batchstep.id] = batchstep.get_dependencies()
    return batchsteps, batchstep_dependency


def optimize_batch(
    obj_batchsteps: list[meta.Batchstep],
    activities: dict[
        uuid.UUID,
        packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage,
    ],
) -> dict[int, list[uuid.UUID]]:
    batchsteps, batchstep_dependency = create_dependency(obj_batchsteps)
    batchstep_to_length = {
        i.id: activities[i.id].get_pipeline_counter() for i in obj_batchsteps
    }
    batchstep_dependency_on, batchstep_dependency_of = transform_batchstep_deps(
        batchstep_dependency
    )
    ind_batchsteps = get_all_independent_batchsteps(batchsteps, batchstep_dependency_on)
    dependency_groups = get_dependency_groups_of_independent_bs(
        ind_batchsteps, batchstep_dependency_on, batchstep_dependency_of
    )
    dep_group_to_len = calculate_length_of_dependency_groups(
        dependency_groups, batchstep_to_length
    )
    return distribute_batchsteps(dep_group_to_len)
