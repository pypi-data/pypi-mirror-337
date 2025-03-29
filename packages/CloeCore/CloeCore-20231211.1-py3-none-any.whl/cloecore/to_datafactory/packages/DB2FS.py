import logging
from typing import Union

import cloecore.utils.model as meta
from cloecore.to_datafactory.arm.datafactory import (
    custom_activities,
    datasets,
    linked_services,
)
from cloecore.to_datafactory.packages.base import Package

logger = logging.getLogger(__name__)


def create_datasets(
    dataset_base_name: str,
    linked_service_fs_container: str,
    db_linked_service: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService
    | linked_services.OracleLinkedService
    | linked_services.SqlServerLinkedService
    | linked_services.DB2LinkedService
    | linked_services.PostgreSQLLinkedService
    | linked_services.AzurePostgreSQLLinkedService,
    fs_linked_service: linked_services.AzureBlobStorageLinkedService,
) -> tuple[
    datasets.AzureSqlDataset
    | datasets.AzureSynapseAnalyticsDataset
    | datasets.SqlServerDataset
    | datasets.SnowflakeDataset
    | datasets.OracleDataset
    | datasets.DB2Dataset
    | datasets.PostgreSQLDataset
    | datasets.AzurePostgreSQLDataset,
    datasets.ParquetDataset,
]:
    folder_name = "DB2FS/source"
    ds_in: Union[
        datasets.AzureSqlDataset,
        datasets.AzureSynapseAnalyticsDataset,
        datasets.SnowflakeDataset,
        datasets.OracleDataset,
        datasets.SqlServerDataset,
        datasets.DB2Dataset,
        datasets.PostgreSQLDataset,
        datasets.AzurePostgreSQLDataset
    ]

    if isinstance(db_linked_service, linked_services.AzureSqlLinkedService):
        ds_in = datasets.AzureSqlDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(
        db_linked_service, linked_services.AzureSynapseAnalyticsLinkedService
    ):
        ds_in = datasets.AzureSynapseAnalyticsDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(db_linked_service, linked_services.SnowflakeLinkedService):
        ds_in = datasets.SnowflakeDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(db_linked_service, linked_services.OracleLinkedService):
        ds_in = datasets.OracleDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(db_linked_service, linked_services.SqlServerLinkedService):
        ds_in = datasets.SqlServerDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(db_linked_service, linked_services.DB2LinkedService):
        ds_in = datasets.DB2Dataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(db_linked_service, linked_services.PostgreSQLLinkedService):
        ds_in = datasets.PostgreSQLDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    elif isinstance(db_linked_service, linked_services.AzurePostgreSQLLinkedService):
        ds_in = datasets.AzurePostgreSQLDataset(
            name=f"{dataset_base_name}_source",
            linked_service=db_linked_service,
            folder_name=folder_name,
        )
    ds_out_location = datasets.AzureBlobLocation(linked_service_fs_container)
    ds_out = datasets.ParquetDataset(
        name=f"{dataset_base_name}_sink",
        linked_service=fs_linked_service,
        location=ds_out_location,
        folder_name="DB2FS/sink",
    )
    return ds_in, ds_out


class DB2FSPackage(Package):
    """Wrapper class to includes all necessary
    classes for a DB2FS package including connections
    and dependencies between them.
    """

    def __init__(
        self,
        job: meta.DB2FS,
        source_ls: linked_services.AzureSqlLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.SnowflakeLinkedService
        | linked_services.OracleLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.DB2LinkedService
        | linked_services.PostgreSQLLinkedService
        | linked_services.AzurePostgreSQLLinkedService,
        sink_ls: linked_services.AzureBlobStorageLinkedService,
        ds_in_schema_name: str,
        ds_in_table_name: str,
        act_in_reader_query: str,
        ds_out_sink_directory: str,
        ds_out_sink_file_name: str,
        datasource_info_id: str,
        datasttype_id: str,
        filestorage_id: str,
        fc_ls: linked_services.AzureSqlLinkedService
        | linked_services.SnowflakeLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService,
        activity_description: str | None = None,
        sequence_column_name: str | None = None,
    ) -> None:
        super().__init__(job.id, job.name)
        self.source_ds, self.sink_ds = create_datasets(
            job.name, job.container_name, source_ls, sink_ls
        )
        self.used_datasets += [self.source_ds, self.sink_ds]
        self.activity_description = activity_description or ""
        self.ds_out_sink_directory = ds_out_sink_directory
        self.sequence_column_name = sequence_column_name
        self.ds_in_schema_name = ds_in_schema_name
        self.ds_in_table_name = ds_in_table_name
        self.act_in_reader_query = act_in_reader_query
        self.datasource_info_id = datasource_info_id
        self.ds_out_sink_file_name = ds_out_sink_file_name
        self.datasttype_id = datasttype_id
        self.filestorage_id = filestorage_id
        self.fc_ls = fc_ls
        self.delta_end_sequence: custom_activities.DeltaGetEndSequence | None = None
        self._init_delta_activities()
        self.set_variable_activity = custom_activities.SetVariableFileName(
            ds_out_sink_file_template=self.ds_out_sink_file_name,
        )
        self.filecatalog_activity = self._init_filecatalog_activity()
        self._init_copy_activity()
        self._init_dependencies()

    def _init_delta_activities(self) -> None:
        self.delta_start_sequence = None
        self.delta_end_sequence = None
        if self.sequence_column_name is not None:
            self.delta_end_sequence = custom_activities.DeltaGetEndSequence(
                source_ds=self.source_ds,
                schema_name=self.ds_in_schema_name,
                table_name=self.ds_in_table_name,
                sequence_column_name=self.sequence_column_name,
            )
            if isinstance(self.fc_ls, linked_services.SnowflakeLinkedService):
                self.delta_start_sequence = custom_activities.DeltaGetStartSequence(
                    linked_service=self.fc_ls,
                    datasource_info_id=self.datasource_info_id,
                    datasttype_id=self.datasttype_id,
                )
            if not isinstance(self.fc_ls, linked_services.SnowflakeLinkedService):
                raise NotImplementedError

    def _init_filecatalog_activity(
        self,
    ) -> Union[
        custom_activities.MSSQLFileCatalogInsertActivity,
        custom_activities.SnowflakeFileCatalogInsertActivity,
    ]:
        if isinstance(
            self.fc_ls,
            (
                linked_services.AzureSqlLinkedService,
                linked_services.AzureSynapseAnalyticsLinkedService,
            ),
        ):
            return custom_activities.MSSQLFileCatalogInsertActivity(
                ds_out_sink_directory=self.ds_out_sink_directory,
                datasource_info_id=self.datasource_info_id,
                datasttype_id=self.datasttype_id,
                sink_file_name_variable=self.set_variable_activity,
                filestorage_id=self.filestorage_id,
                linked_service=self.fc_ls,
                sequence_column_name=self.sequence_column_name,
                delta_end_sequence=self.delta_end_sequence,
            )
        elif isinstance(self.fc_ls, linked_services.SnowflakeLinkedService):
            return custom_activities.SnowflakeFileCatalogInsertActivity(
                ds_out_sink_directory=self.ds_out_sink_directory,
                datasource_info_id=self.datasource_info_id,
                datasttype_id=self.datasttype_id,
                sink_file_name_variable=self.set_variable_activity,
                filestorage_id=self.filestorage_id,
                linked_service=self.fc_ls,
                sequence_column_name=self.sequence_column_name,
                delta_end_sequence=self.delta_end_sequence,
            )

    def _init_copy_activity(self) -> None:
        self.copy_activity = custom_activities.DB2FSCopyActivity(
            description=self.activity_description,
            source_ds=self.source_ds,
            source_schema_name=self.ds_in_schema_name,
            source_table_name=self.ds_in_table_name,
            source_sql_reader_query=self.act_in_reader_query,
            sink_ds=self.sink_ds,
            sink_file_path=self.ds_out_sink_directory,
            sink_file_name_variable=self.set_variable_activity,
            delta_end_sequence=self.delta_end_sequence,
            delta_start_sequence=self.delta_start_sequence,
            sequence_column_name=self.sequence_column_name,
        )

    def _init_dependencies(self) -> None:
        if self.delta_end_sequence is None or self.delta_start_sequence is None:
            self.copy_activity.add_activity_dependency(
                self.set_variable_activity, "Succeeded"
            )
        else:
            self.delta_end_sequence.add_activity_dependency(
                self.set_variable_activity, "Succeeded"
            )
            self.delta_start_sequence.add_activity_dependency(
                self.set_variable_activity, "Succeeded"
            )
            self.copy_activity.add_activity_dependency(
                self.delta_end_sequence, "Succeeded"
            )
            self.copy_activity.add_activity_dependency(
                self.delta_start_sequence, "Succeeded"
            )
        self.filecatalog_activity.add_activity_dependency(
            self.copy_activity, "Succeeded"
        )
        self.start_activity = self.set_variable_activity
        self.end_activity = self.filecatalog_activity
        self.all_activities = [
            self.set_variable_activity,
            self.copy_activity,
            self.filecatalog_activity,
        ]
        self.pipeline_activities = [
            self.set_variable_activity,
            self.copy_activity,
            self.filecatalog_activity,
        ]
        if self.delta_start_sequence is not None:
            self.all_activities.append(self.delta_start_sequence)
            self.pipeline_activities.append(self.delta_start_sequence)
        if self.delta_end_sequence is not None:
            self.all_activities.append(self.delta_end_sequence)
            self.pipeline_activities.append(self.delta_end_sequence)
