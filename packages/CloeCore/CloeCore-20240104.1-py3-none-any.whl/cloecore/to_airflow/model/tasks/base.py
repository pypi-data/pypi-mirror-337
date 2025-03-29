import uuid


class BaseTask:
    """Base class for all airflow tasks."""

    library: str = ""
    imports: str = ""

    def __init__(
        self, name: str, task_n: uuid.UUID, depends_on: list[uuid.UUID]
    ) -> None:
        self.task_name: str = name
        self.task_n: uuid.UUID = task_n
        self.depends_on: list[uuid.UUID] = depends_on

    def to_python_libraries(self) -> str:
        return f"from {self.library} import {self.imports}"

    def to_dependencies(self) -> list:
        return [
            f"t{str(self.task_n).replace('-', '')} << t{str(dep).replace('-', '')}"
            for dep in self.depends_on
        ]

    def to_python(self) -> str:
        return f"t{str(self.task_n).replace('-', '')} = print('hello world')"
