import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_tenant_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> meta.Tenants:
    tenants: list[meta.Tenant] = []
    raw_model_json = models.pop("repository.tenant", [])
    for raw_tenant in raw_model_json:
        try:
            tenant = meta.Tenant(**raw_tenant)
            tenants.append(tenant)
        except ValidationError as error:
            error_name = f"{raw_tenant.get('name', str(uuid.uuid4()))}"
            errors.tenants[error_name] = error
    try:
        return meta.Tenants(tenants=tenants)
    except ValidationError as error:
        errors.tenants["Tenants"] = error
        return meta.Tenants()
