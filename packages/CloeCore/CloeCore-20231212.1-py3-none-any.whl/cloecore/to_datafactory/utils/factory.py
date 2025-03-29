import logging
import uuid
from collections import deque

import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def sort_objects_into_groups(batchsteps: list[meta.Batchstep]) -> list[list[uuid.UUID]]:
    # Create a mapping from object IDs to ObjectNodes
    obj_dict = {obj.id: obj for obj in batchsteps}

    # Function to find connected components (groups of dependent objects)
    def find_connected_component(
        start_id: uuid.UUID, visited: set[uuid.UUID]
    ) -> list[uuid.UUID]:
        component = []
        queue = deque([start_id])

        while queue:
            current_id = queue.popleft()
            if current_id not in visited:
                visited.add(current_id)
                component.append(current_id)

                # Add dependencies to the queue
                current_deps_raw = obj_dict[current_id].dependencies
                current_deps = [] if current_deps_raw is None else current_deps_raw
                for dep in sorted(
                    [dep.dependent_on_batchstep_id for dep in current_deps]
                ):
                    if dep not in visited:
                        queue.append(dep)

        return sorted(component)

    # Find all connected components
    visited: set[uuid.UUID] = set()
    groups = []
    for obj in sorted(batchsteps, key=lambda x: x.id):
        if obj.id not in visited:
            component = find_connected_component(obj.id, visited)
            groups.append(component)

    # Ensure each group has at most 40 objects
    final_groups = []
    for group in groups:
        for i in range(0, len(group), 40):
            final_groups.append(group[i : i + 40])

    return final_groups


def minimize_groups(groups: list[list[uuid.UUID]]) -> list[list[uuid.UUID]]:
    collapsed_groups: list[list[uuid.UUID]] = []
    for group in sorted(groups, key=lambda x: (len(x), x)):
        # Try to merge the current group with any of the collapsed groups
        merged = False
        for c_group in collapsed_groups:
            if len(c_group) + len(group) <= 40:
                c_group.extend(group)
                merged = True
                break
        if not merged:
            collapsed_groups.append(group)
    return collapsed_groups


def optimize_batch(
    obj_batchsteps: list[meta.Batchstep],
) -> dict[int, list[uuid.UUID]]:
    dependency_groups = sort_objects_into_groups(obj_batchsteps)
    dependency_groups = minimize_groups(dependency_groups)
    return {i: j for i, j in enumerate(dependency_groups)}
