from cloecore.to_datafactory.arm.datafactory.datasets.base import DatasetResource
from cloecore.to_datafactory.arm.datafactory.linked_services import base


class AzureBlobLocation:
    type = "AzureBlobStorageLocation"

    def __init__(self, container_name: str) -> None:
        self.container_name = container_name

    def _get_parameter_expression(self, name: str) -> dict:
        return {"value": f"@dataset().{name}", "type": "Expression"}

    def to_arm(self) -> dict[str, str | dict]:
        return {
            "type": self.type,
            "folderPath": self._get_parameter_expression("folderPath"),
            "fileName": self._get_parameter_expression("fileName"),
            "container": self.container_name,
        }


class FileDataset(DatasetResource):
    file_type: str = "Default"

    def __init__(
        self,
        name: str,
        linked_service: base.LinkedServiceBase,
        folder_name: str,
        annotations: list[str] | None = None,
        schema: list | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name,
            linked_service,
            folder_name,
            annotations,
            schema,
            required_arm_variables,
        )
        self.type_properties: dict = {}
        self._create_parameter(name="folderPath")
        self._create_parameter(name="fileName")

    def _to_arm(self) -> dict:
        return {"type": self.file_type, "typeProperties": self.type_properties}

    def to_arm(self) -> dict[str, dict | str | list]:
        self.properties = self._to_arm()
        return super().to_arm()


class ParquetDataset(FileDataset):
    file_type = "Parquet"
    compression_codec = "snappy"

    def __init__(self, *args, location: AzureBlobLocation, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.location = location

    def _to_arm(self) -> dict[str, dict | str | list]:
        return {
            "type": self.file_type,
            "typeProperties": {
                "location": self.location.to_arm(),
                "compressionCodec": self.compression_codec,
            },
            "annotations": self.annotations,
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        self.type_properties = self._to_arm()
        return super().to_arm()
