import logging
import uuid

import cloecore.utils.model as meta
from cloecore.to_datafactory.arm.datafactory import linked_services

logger = logging.getLogger(__name__)


def model_conn_to_linked_service(
    connections: dict[uuid.UUID, meta.Connection],
) -> tuple[
    linked_services.AzureKeyVaultLinkedService,
    linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService
    | None,
    dict[
        uuid.UUID,
        linked_services.AzureBlobStorageLinkedService
        | linked_services.AzureSqlLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.OracleLinkedService
        | linked_services.SnowflakeLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.DB2LinkedService
        | linked_services.PostgreSQLLinkedService
        | linked_services.AzurePostgreSQLLinkedService,
    ],
]:
    conn_id_to_ls: dict[
        uuid.UUID,
        linked_services.AzureBlobStorageLinkedService
        | linked_services.AzureSqlLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.OracleLinkedService
        | linked_services.SnowflakeLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.DB2LinkedService
        | linked_services.PostgreSQLLinkedService
        | linked_services.AzurePostgreSQLLinkedService,
    ] = {}
    secret_store = linked_services.AzureKeyVaultLinkedService()
    fc_ls = None
    for connection in connections.values():
        if connection.is_azure_blob:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[
                connection.id
            ] = linked_services.AzureBlobStorageLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_azure_sql_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.AzureSqlLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_synapse_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[
                connection.id
            ] = linked_services.AzureSynapseAnalyticsLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_oracle_db:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.OracleLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_snowflake_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.SnowflakeLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_sql_server_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.SqlServerLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_db2_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.DB2LinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_postgres_sql_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.PostgreSQLLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        elif connection.is_azurepostgres_sql_nativ:
            secret_reference = secret_store.get_secret_reference(
                connection.connection_string_secret_name
            )
            conn_id_to_ls[connection.id] = linked_services.AzurePostgreSQLLinkedService(
                name=connection.name,
                connection=connection,
                secret_reference=secret_reference,
                depends_on=secret_store.get_dependency_on(),
            )
        else:
            logger.error("Unknown Connection Service type %s", connection.system_type)
            raise NotImplementedError
        if connection.is_file_catalog_connection:
            fc_ls_check = conn_id_to_ls[connection.id]
            if not isinstance(
                fc_ls_check,
                (
                    linked_services.AzureSqlLinkedService,
                    linked_services.AzureSynapseAnalyticsLinkedService,
                    linked_services.SnowflakeLinkedService,
                ),
            ):
                raise NotImplementedError
            fc_ls = fc_ls_check
    return secret_store, fc_ls, conn_id_to_ls
