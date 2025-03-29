import logging

logger = logging.getLogger(__name__)


class AzureBlobSink:
    """Base class for all azure blob based sinks in copy
    activities.

    Returns:
        _type_: _description_
    """

    store_type: str = "AzureBlobStorageWriteSettings"
    file_type: str = "Default"

    def to_arm(self) -> dict[str, dict | str | list]:
        return {"type": self.file_type, "storeSettings": {"type": self.store_type}}


class ParquetSink(AzureBlobSink):
    file_type = "ParquetSink"


class SqlSink:
    """Base class for all sql based sinks in copy
    activities.

    Returns:
        _type_: _description_
    """

    sql_type: str = "Default"

    def __init__(self, precopy_script: str | None = None) -> None:
        self.precopy_script = precopy_script

    def to_arm(self) -> dict[str, dict | str | list]:
        base: dict[str, dict | str | list] = {"type": self.sql_type}
        if self.precopy_script is not None:
            base["preCopyScript"] = self.precopy_script
        return base


class AzureSqlSink(SqlSink):
    """SQLSink Wrapper class resembling
    Azure SQL sink
    """

    sql_type = "AzureSqlSink"


class AzureSynapseAnalyticsSink:
    sql_type = "SqlDWSink"

    def __init__(self, precopy_script: str | None = None) -> None:
        self.precopy_script = precopy_script

    def to_arm(self) -> dict[str, dict | str | bool]:
        base: dict[str, dict | str | bool] = {
            "type": "SqlDWSink",
            "allowPolyBase": True,
            "polyBaseSettings": {
                "rejectType": "percentage",
                "rejectValue": 10.0,
                "rejectSampleValue": 100,
                "useTypeDefault": True,
            },
        }
        if self.precopy_script is not None:
            base["preCopyScript"] = self.precopy_script
        return base


class SnowflakeSink(SqlSink):
    sql_type = "SnowflakeSink"

    def to_arm(self) -> dict[str, dict | str | list]:
        base = super().to_arm()
        base["importSettings"] = {
            "type": "SnowflakeImportCopyCommand",
            "copyOptions": {
                "FORCE": "TRUE",
                "ON_ERROR": "SKIP_FILE",
            },
            "fileFormatOptions": {
                "DATE_FORMAT": "YYYY-MM-DD",
            },
        }
        return base
