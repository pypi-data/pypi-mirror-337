from jinja2.environment import Template

from cloecore.utils.model.jobs import exec_sql
from cloecore.utils.model.modeler.simple_pipe import SimplePipe, SPTableMapping


class SimplePipeGenerator:
    """SimplePipe metadata to sql generator class."""

    def __init__(self, simple_pipe: SimplePipe) -> None:
        self.name = simple_pipe.name
        self.job_id = simple_pipe.job_id
        self.sqlpipe_statement: Template = Template(simple_pipe.sql_pipe_template)
        self.table_mapping: list[SPTableMapping] = simple_pipe.table_mappings

    def _gen(self, mapping: SPTableMapping, return_queries_as_string: bool) -> str:
        mapping.source_table.render_flag = return_queries_as_string
        mapping.sink_table.render_flag = return_queries_as_string
        anchors = {
            "source_table": mapping.source_table.get_table_identifier(),
            "sink_table": mapping.sink_table.get_table_identifier(),
        }
        template = self.sqlpipe_statement.render(anchors)
        return template

    def gen_script(self) -> str:
        """Generates a sql script or exec_sql job json snippet.

        Args:
            return_queries_as_string (bool | None, optional): _description_.
            Defaults to True.

        Returns:
            str: _description_
        """
        queries = {}
        for mapping in self.table_mapping:
            queries[mapping.order_by] = self._gen(mapping, True)
        return "\n\n-- NEXT TABLE STARTING \n".join(
            [queries[i] for i in sorted(queries)]
        )

    def gen_job(self) -> list[exec_sql.ExecSQLRuntime]:
        """Generates a sql script or exec_sql job json snippet.

        Args:
            return_queries_as_string (bool | None, optional): _description_.
            Defaults to True.

        Returns:
            str: _description_
        """
        queries = []
        for mapping in self.table_mapping:
            source_identifier = mapping.source_table.get_table_identifier()
            sink_identifier = mapping.sink_table.get_table_identifier()
            runtime_query = self._gen(mapping, False)
            split_queries = [
                sub_query.strip()
                for sub_query in runtime_query.split(";")
                if sub_query is not None and len(sub_query) > 1
            ]
            split_queries = split_queries if len(split_queries) > 1 else [runtime_query]
            for order_number, query in enumerate(split_queries):
                exec_sql_query = exec_sql.ExecSQLRuntime(
                    query=query,
                    exec_order=int(f"{order_number}{mapping.order_by}"),
                    description=f"{source_identifier} TO {sink_identifier}",
                )
                queries.append(exec_sql_query)
        return queries
