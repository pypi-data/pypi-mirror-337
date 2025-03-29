import importlib.resources as pkg_resources

from cloecore.utils.model.modeler.templates import SQLTemplates


class EngineTemplates:
    def __init__(self, sql_language: str) -> None:
        resource = f"cloecore.to_sql.sql.Templates.{sql_language}.engine"
        self.bk_generation: str = pkg_resources.read_text(
            resource, "bk_generation.sql.j2"
        )
        self.dq1_view_ddl: str = pkg_resources.read_text(
            resource, "dq1_view_ddl.sql.j2"
        )
        self.dq2_view_ddl: str = pkg_resources.read_text(
            resource, "dq2_view_ddl.sql.j2"
        )
        self.dq3_view_ddl: str = pkg_resources.read_text(
            resource, "dq3_view_ddl.sql.j2"
        )
        self.dq2_error_logging: str = pkg_resources.read_text(
            resource, "dq2_error_logging.sql.j2"
        )
        self.dq3_error_logging: str = pkg_resources.read_text(
            resource, "dq3_error_logging.sql.j2"
        )
        self.hashing_function: str = pkg_resources.read_text(
            resource, "hashing_function.sql.j2"
        )
        self.lookup_join: str = pkg_resources.read_text(resource, "lookup_join.sql.j2")
        self.null_handling: str = pkg_resources.read_text(
            resource, "null_handling.sql.j2"
        )
        self.dq1_error_logging: str = pkg_resources.read_text(
            resource, "dq1_error_logging.sql.j2"
        )
        self.id_to_attribute: dict[int, str] = {
            1: "bk_generation",
            2: "dq1_view_ddl",
            3: "dq2_view_ddl",
            4: "dq3_view_ddl",
            5: "dq2_error_logging",
            6: "dq3_error_logging",
            7: "hashing_function",
            8: "lookup_join",
            9: "null_handling",
            10: "dq1_error_logging",
        }

    def merge_custom_templates(self, custom_templates: SQLTemplates) -> None:
        for template in custom_templates.sqltemplates:
            if template.id in self.id_to_attribute:
                self.__setattr__(self.id_to_attribute[template.id], template.template)
