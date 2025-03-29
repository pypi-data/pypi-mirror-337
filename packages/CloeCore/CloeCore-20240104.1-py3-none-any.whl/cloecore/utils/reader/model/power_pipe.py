import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.model.modeler as modeler
import cloecore.utils.model.modeler.powerpipe as pp


def read_raw_powerpipe_lookup(
    raw_lookup: dict,
    databases: meta.Databases,
    engine_templates: modeler.SQLTemplates,
) -> pp.PPLookup | custom_errors.PowerPipeLookupError:
    errors = custom_errors.PowerPipeLookupError(
        f"lu_{raw_lookup.get('name', str(uuid.uuid4()))}"
    )
    lu_parameters = []
    rc_mappings = []
    for l_parameter in raw_lookup.pop("lookup_parameters", []):
        try:
            lu_parameters.append(pp.PPLookupParameter(**l_parameter))
        except ValidationError as error:
            errors.parameter_mapping.append(error)
    for rc_mapping in raw_lookup.pop("return_column_mappings", []):
        try:
            rc_mappings.append(
                pp.PPLookupReturnColumnMapping(
                    **rc_mapping,
                    tables=databases.tables,
                )
            )
        except ValidationError as error:
            errors.return_column_mapping[rc_mapping.get("name", uuid.uuid4())] = error
    try:
        lookup = pp.PPLookup(
            **raw_lookup,
            tables=databases.tables,
            engine_templates=engine_templates,
            return_column_mappings=rc_mappings,
            lookup_parameters=lu_parameters,
        )
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else lookup


def read_raw_powerpipe(
    raw_powerpipe: dict,
    databases: meta.Databases,
    engine_templates: modeler.SQLTemplates,
    tenants: meta.Tenants,
    sql_templates: modeler.SQLTemplates,
    conversion_templates: modeler.ConversionTemplates,
) -> pp.PowerPipe | custom_errors.PowerPipeError:
    errors = custom_errors.PowerPipeError(raw_powerpipe.get("name", str(uuid.uuid4())))
    lookups = []
    column_mappings = []
    source_tables = []
    for raw_lu in raw_powerpipe.pop("lookups", []):
        lookup = read_raw_powerpipe_lookup(
            raw_lu, databases=databases, engine_templates=engine_templates
        )
        if isinstance(lookup, custom_errors.PowerPipeLookupError):
            errors.lookups.append(lookup)
        else:
            lookups.append(lookup)
    for raw_cm in raw_powerpipe.pop("column_mappings", []):
        try:
            cm = pp.PPColumnMapping(
                **raw_cm, tables=databases.tables, conversions=conversion_templates
            )
            column_mappings.append(cm)
        except ValidationError as error:
            error_name = f"cm_{raw_cm.get('source_column_name', str(uuid.uuid4()))}"
            errors.column_mapping[error_name] = error
    for raw_st in raw_powerpipe.pop("source_tables", []):
        try:
            st = pp.PPSourceTable(
                **raw_st,
                tables=databases.tables,
                tenants=tenants,
                column_mappings=column_mappings,
            )
            source_tables.append(st)
        except ValidationError as error:
            error_name = f"st_{raw_st.get('table_id', str(uuid.uuid4()))}"
            errors.source_tables[error_name] = error
    try:
        pipe = pp.PowerPipe(
            **raw_powerpipe,
            source_tables=source_tables,
            tables=databases.tables,
            column_mappings=column_mappings,
            lookups=lookups,
            templates=sql_templates,
            engine_templates=engine_templates,
        )
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else pipe
