import logging
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, Field, validator

from cloecore.utils import templating_engine, writer
from cloecore.utils.model.jobs.base import BaseJob
from cloecore.utils.model.jobs.connections import Connection, Connections

logger = logging.getLogger(__name__)


class ExecSQLRuntime(BaseModel):
    """Base class for loading CLOE query model objects."""

    no_render: bool = Field(default=False, exclude=True)
    exec_order: int
    query: str
    description: str | None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

    @validator("query", pre=True)
    def valid_jinja2_template(cls, value, values, **kwargs):
        try:
            if values["no_render"]:
                Template(value, variable_start_string="[[", variable_end_string="]]")
            else:
                templating_engine.get_jinja_env().from_string(value)
        except TemplateSyntaxError:
            raise ValueError("template is no valid jinja2 template")
        return value

    def get_rendered_runtime(self) -> str:
        template = templating_engine.get_jinja_env().from_string(self.query)
        return template.render()


class ExecSQLJob(BaseJob):
    """Base class for loading CLOE ExecSQLJob model objects."""

    connections: Connections = Field(..., exclude=True)
    connection_id: uuid.UUID
    queries: list[ExecSQLRuntime]
    sp_schema: str = Field(default="cloe_dwh", exclude=True)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

    @validator("queries")
    def runtimes_order_by_unique_check(cls, value: list[ExecSQLRuntime]):
        order_number = []
        for query in value:
            if query.exec_order not in order_number:
                order_number.append(query.exec_order)
            else:
                raise ValueError("ExecSQLRuntime exec_order not unique")
        return value

    @validator("connection_id")
    def sink_connection_exists(cls, value, values, **kwargs):
        if "connections" in values and not values[
            "connections"
        ].check_if_connection_exists_by_id(value):
            raise ValueError("connection_id not in connections")
        return value

    @property
    def sink_connection(self) -> Connection:
        return self.connections.get_connection_by_id(self.connection_id)

    def get_rendered_runtimes(self) -> list[str]:
        return [
            query.get_rendered_runtime()
            for query in sorted(self.queries, key=lambda x: x.exec_order)
        ]

    def get_procedure_name(self) -> str:
        return f"sp_{self.name}".lower().replace(" ", "_")

    def get_procedure_identifier(self) -> str:
        return self.sink_connection.get_object_identifier(
            self.sp_schema, self.get_procedure_name()
        )

    def get_procedure_call_query(self) -> str:
        return self.sink_connection.get_procedure_call(
            self.sp_schema, self.get_procedure_name()
        )

    def get_procedure_call_query_with_parameters(
        self, parameters: dict[str, str]
    ) -> str:
        connection = self.sink_connection
        return connection.get_procedure_call_with_parameters(
            self.sp_schema, self.get_procedure_name(), parameters
        )

    def get_procedure_create_query(self, is_transaction: bool = False) -> str:
        connection = self.sink_connection
        query = connection.get_procedure_create(
            self.sp_schema,
            self.get_procedure_name(),
            self.get_rendered_runtimes(),
            is_transaction,
        )
        return f"{query}{self.sink_connection.get_query_postfix()}"


class ExecSQLJobs(BaseModel):
    model_id: str = "jobs.exec_sql"
    model_content: list[ExecSQLJob]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase
