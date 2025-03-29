import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.batch as bat


def read_raw_batchstep(raw_step: dict) -> bat.Batchstep | custom_errors.BatchstepError:
    errors = custom_errors.BatchstepError(raw_step.get("name", str(uuid.uuid4())))
    dependencies = []
    for raw_dep in raw_step.pop("dependencies", []):
        try:
            dep = bat.BatchstepDependency(**raw_dep)
            dependencies.append(dep)
        except ValidationError as error:
            errors.dependencies.append(error)
    try:
        batchstep = bat.Batchstep(
            **raw_step,
            dependencies=dependencies,
        )
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else batchstep


def read_raw_batch(
    raw_batch: dict,
) -> bat.Batch | custom_errors.BatchError:
    errors = custom_errors.BatchError(raw_batch.get("name", str(uuid.uuid4())))
    batchsteps = []
    for raw_step in raw_batch.pop("batchsteps", []):
        step = read_raw_batchstep(raw_step)
        if isinstance(step, custom_errors.BatchstepError):
            errors.batchstep_error.append(step)
        else:
            batchsteps.append(step)
    try:
        batch = bat.Batch(**raw_batch, batchsteps=batchsteps)
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else batch
