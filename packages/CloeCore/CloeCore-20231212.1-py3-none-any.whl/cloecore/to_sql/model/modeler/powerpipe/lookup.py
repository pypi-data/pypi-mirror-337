import logging

from jinja2 import environment

from cloecore.to_sql import utils
from cloecore.to_sql.sql.sql_syntax import SQLSyntax
from cloecore.utils.model.modeler.powerpipe.Lookups import (
    PPLookup,
    PPLookupReturnColumnMapping,
)

logger = logging.getLogger(__name__)


class PPLookupReturnColumnMappingGenerator:
    """Generates and controls powerpipe lookup column return
    level snippet generation.
    """

    def __init__(
        self,
        lookup_return_columnampping: PPLookupReturnColumnMapping,
        lookup_id: int,
        lookup_name: str,
        artifacts: utils.Artifacts,
        sql_syntax: SQLSyntax,
    ) -> None:
        self.sink_table_id = lookup_return_columnampping.sink_table_id
        self.sink_table = lookup_return_columnampping.sink_table
        self.lookup_id = lookup_id
        self.lookup_name = lookup_name
        self.artifacts = artifacts
        self.is_insert = lookup_return_columnampping.is_insert
        self.is_logging_on_lookup_error = (
            lookup_return_columnampping.is_logging_on_lookup_error
        )
        self.is_update = lookup_return_columnampping.is_update
        self.on_null_value = lookup_return_columnampping.on_null_value
        self.source_column_name = lookup_return_columnampping.return_column_name
        self.sink_column_name = lookup_return_columnampping.sink_column_name
        self.sql_syntax = sql_syntax

    @property
    def source_column_identifier(self) -> str:
        name = self.sql_syntax.column_identifier(self.source_column_name)
        return f"l{self.lookup_id}.{name}"

    @property
    def sink_column_identifier(self) -> str:
        if self.sink_table.is_version:
            return f"ver.{self.sql_syntax.column_identifier(self.sink_column_name)}"
        return f"t.{self.sql_syntax.column_identifier(self.sink_column_name)}"

    @property
    def table_identifier(self) -> str:
        return self.sink_table.get_table_identifier()

    @property
    def is_version(self) -> bool:
        return self.sink_table.is_version

    def _get_column_base(
        self,
        null_check_template: environment.Template | None = None,
        with_null_handling: bool = False,
    ) -> str:
        """Generates the column that need to be used by all methods which reference the
        column including null handling.

        Args:
            null_check_template (environment.Template): _description_
            with_null_handling (bool | None, optional): _description_.
            Defaults to False.

        Raises:
            SystemExit: _description_

        Returns:
            str: _description_
        """
        if (
            with_null_handling
            and self.on_null_value is not None
            and null_check_template is not None
        ):
            return self.sql_syntax.column_nullhandling(
                column_name=self.source_column_identifier,
                null_check_template=null_check_template,
                alternative_value=self.on_null_value,
            )
        if with_null_handling and self.on_null_value is None:
            logger.error(
                (
                    "Null handling(DQ3) for return column mapping %s/%s"
                    "activated but no on_null_value defined."
                ),
                self.source_column_name,
                self.sink_column_name,
            )
            raise SystemExit("Logic error in model. Please check logging output.")
        return self.source_column_identifier

    def _get_null_check(self) -> str:
        """Generates a null check snippet. It compares it checks
        both the sink and source column for null values and wraps them
        in an "and" logic check.

        Args:
            prioritize_name (bool): _description_

        Returns:
            str: _description_
        """
        return self.sql_syntax.condition_comparison_and(
            self.sql_syntax.column_is_null(self.sink_column_identifier),
            self.sql_syntax.column_is_null(self._get_column_base(), is_not=True),
            with_brackets=True,
        )

    def _gen_dq_snippets(self, null_check_template: environment.Template) -> None:
        """Generates data quality snippets for dq3 views.

        Args:
            null_check_template (environment.Template): _description_
        """
        if self.is_insert or self.is_update:
            self.artifacts.dq3_view_select_as_raw.append(
                self.sql_syntax.column_alias(
                    self._get_column_base(null_check_template, with_null_handling=True),
                    self.sink_column_name,
                )
            )
            if self.is_logging_on_lookup_error:
                self.artifacts.dq3_log_select.append(
                    self._get_column_base(with_null_handling=False)
                )
                self.artifacts.dq3_log_where.append(
                    self.sql_syntax.column_is_null(
                        self._get_column_base(with_null_handling=False)
                    )
                )

    def _gen_lookup_snippets(self, null_check_template: environment.Template) -> None:
        """Generates base snippets for lookup base insert/updates.

        Args:
            null_check_template (environment.Template): _description_
        """
        source_column_artifact = self._get_column_base(
            null_check_template,
            with_null_handling=self.artifacts.include_dq3,
        )
        if not self.is_version:
            self.artifacts.source_lu_used_columns.append(self.source_column_identifier)
            if self.is_insert:
                self.artifacts.lu_source_insert.append(source_column_artifact)
                self.artifacts.lu_sink_insert.append(self.sink_column_name)
            if self.is_update:
                self.artifacts.sink_source_field_comparison.append(
                    self.sql_syntax.column_comparison_difference(
                        self.sink_column_identifier, source_column_artifact
                    )
                )
                self.artifacts.lu_sink_source_update.append(
                    self.sql_syntax.column_comparison_equality(
                        self.sink_column_name, source_column_artifact
                    )
                )
        column_compare_artifact = self.sql_syntax.column_comparison_difference(
            self.sink_column_identifier, source_column_artifact
        )
        if self.is_version:
            self.artifacts.versioning_artifacts[
                self.table_identifier
            ].ver_source_insert.append(source_column_artifact)
            self.artifacts.versioning_artifacts[
                self.table_identifier
            ].ver_sink_insert.append(self.sink_column_name)
            if self.is_update:
                self.artifacts.versioning_artifacts[
                    self.table_identifier
                ].ver_sink_source_field_comparison.append(
                    self.sql_syntax.condition_comparison_or(
                        column_compare_artifact,
                        self._get_null_check(),
                        with_brackets=True,
                    )
                )

    def gen(self, null_check_template: environment.Template) -> None:
        """Main entry method for generating all snippets of lookup column mapping
        and add them to the template global environment.

        Args:
            null_check_template (environment.Template): _description_
            template_env (environment.Environment): _description_
        """
        self._gen_lookup_snippets(null_check_template)
        if self.artifacts.include_dq3:
            self._gen_dq_snippets(null_check_template)


class PPLookupGenerator:
    """Generates and controls powerpipe lookup snippet generation."""

    def __init__(
        self,
        lookup: PPLookup,
        lookup_id: int,
        sql_syntax: SQLSyntax,
        artifacts: utils.Artifacts,
        template_environment: environment.Environment,
    ) -> None:
        self.name = lookup.name
        self.rendered_sink_bk_name = lookup.rendered_sink_bk_name
        self.lookup_id = lookup_id
        self.lookup_table_id = lookup.lookup_table_id
        self.is_add_tenant_to_lookup_parameter = (
            lookup.is_add_tenant_to_lookup_parameter
        )
        self.lu_column_name_artifact = lookup.lookup_column_name
        self.lu_valid_parametercolumn_name_artifact = (
            lookup.lookup_valid_parameter_column_name
        )
        self.lu_valid_fromcolumn_name_artifact = lookup.lookup_valid_from_column_name
        self.lu_valid_tocolumn_name_artifact = lookup.lookup_valid_to_column_name
        self.lookup_source_table = lookup.lookup_source_table
        self.template_env = template_environment
        self.artifacts = artifacts
        self.sql_syntax = sql_syntax
        self.lookup_parameters = lookup.lookup_parameters
        self.return_column_mappings = [
            PPLookupReturnColumnMappingGenerator(
                i, lookup_id, lookup.name, artifacts, sql_syntax
            )
            for i in lookup.return_column_mappings
        ]
        self.artifacts.versioning_artifacts |= {
            mapping.table_identifier: utils.VersionArtifact(
                sql_syntax=sql_syntax,
                sink_table_identifier=mapping.table_identifier,
            )
            for mapping in self.return_column_mappings
            if mapping.is_version
        }

    @property
    def has_logging(self) -> bool:
        """Checks if any of the mappings is suing logging on lookup error.

        Returns:
            bool: _description_
        """
        for mapping in self.return_column_mappings:
            if mapping.is_logging_on_lookup_error:
                return True
        return False

    @property
    def has_version(self) -> bool:
        """Checks if any of the mappings is suing logging on lookup error.

        Returns:
            bool: _description_
        """
        for mapping in self.return_column_mappings:
            if mapping.is_version:
                return True
        return False

    def get_bk_snippet(self, tenant: str | None = None) -> str:
        """Generates the business key(bk) snippet for the lookup bk. Also
        dealing with different tenant options.

        Args:
            tenant (str): _description_

        Raises:
            SystemExit: _description_

        Returns:
            str: _description_
        """
        enumerated_params = {}
        for parameter in self.lookup_parameters:
            if parameter.calculation is not None and not (
                self.artifacts.include_dq1 or self.artifacts.include_dq2
            ):
                enumerated_params[parameter.order_by] = f"!{parameter.calculation}"
            else:
                enumerated_params[
                    parameter.order_by
                ] = self.sql_syntax.column_identifier(parameter.source_column_name)
        params = [enumerated_params[i] for i in sorted(enumerated_params)]
        if self.is_add_tenant_to_lookup_parameter and tenant is None:
            return self.template_env.from_string(
                self.sql_syntax.engine_templates.bk_generation
            ).render(bks=params, tenant="0")
        if not self.is_add_tenant_to_lookup_parameter:
            return self.template_env.from_string(
                self.sql_syntax.engine_templates.bk_generation
            ).render(bks=params)
        return self.template_env.from_string(
            self.sql_syntax.engine_templates.bk_generation
        ).render(bks=params, tenant=tenant)

    def get_join_snippet(self, tenant: str | None = None) -> str:
        """Generates the lookup join.

        Args:
            tenant (str): _description_

        Returns:
            str: _description_
        """
        table_identifier = self.lookup_source_table.get_table_identifier()
        join_template = self.template_env.from_string(
            self.sql_syntax.engine_templates.lookup_join
        )
        lu_valid_pmcna = self.lu_valid_parametercolumn_name_artifact
        return join_template.render(
            table_identifier=table_identifier,
            lookup_id=self.lookup_id,
            lu_valid_parametercolumn_name_artifact=lu_valid_pmcna,
            lu_valid_fromcolumn_name_artifact=self.lu_valid_fromcolumn_name_artifact,
            lu_valid_tocolumn_name_artifact=self.lu_valid_tocolumn_name_artifact,
            lu_column_name_artifact=self.lu_column_name_artifact,
            lu_bk_artifact_artifact=self.get_bk_snippet(tenant),
        )

    def gen_rcm_snippets(self) -> None:
        """Gernerates all return column mapping snippets"""
        for mapping in self.return_column_mappings:
            mapping.gen(
                self.template_env.from_string(
                    self.sql_syntax.engine_templates.null_handling
                )
            )

    def _gen_bk_snippets_ver(
        self, bk_sink_insert: str, tenant: str | None = None
    ) -> None:
        for mapping in self.return_column_mappings:
            if mapping.is_version:
                self.artifacts.versioning_artifacts[
                    mapping.table_identifier
                ].ver_sink_insert.append(bk_sink_insert)
                self.artifacts.versioning_artifacts[
                    mapping.table_identifier
                ].ver_source_insert.append(self.get_bk_snippet(tenant))

    def _gen_bk_snippets(self, tenant: str | None = None) -> None:
        """Calls all bk related snippet generation functions using the table tenant and
        adds snippets to the template global environment.

        Args:
            tenant (str): _description_
        """
        for parameter in self.lookup_parameters:
            name = self.sql_syntax.column_identifier(parameter.source_column_name)
            if parameter.calculation is not None:
                calc_or_name = self.sql_syntax.column_alias(parameter.calculation, name)
            else:
                calc_or_name = f"s.{name}"
            alias_or_name = f"s.{name}"
            self.artifacts.source_lu_used_columns.append(calc_or_name)
            self.artifacts.dq1_view_select_as_raw.append(calc_or_name)
            self.artifacts.dq1_view_select_as_name.append(alias_or_name)
            self.artifacts.dq2_view_select_as_raw.append(
                calc_or_name if not self.artifacts.include_dq1 else alias_or_name
            )
            self.artifacts.dq2_view_select_as_name.append(alias_or_name)
            self.artifacts.dq3_view_select_as_raw.append(
                calc_or_name
                if not (self.artifacts.include_dq1 or self.artifacts.include_dq2)
                else alias_or_name
            )
            self.artifacts.dq3_view_select_as_name.append(alias_or_name)
        bk_source_insert = self.sql_syntax.column_alias(
            self.get_bk_snippet(tenant), self.rendered_sink_bk_name
        )
        bk_sink_insert = self.rendered_sink_bk_name
        self.artifacts.lu_source_insert.append(self.get_bk_snippet(tenant))
        self.artifacts.dq3_view_select_as_raw.append(bk_source_insert)
        self.artifacts.lu_sink_insert.append(bk_sink_insert)
        self.artifacts.lu_sink_source_update.append(
            self.sql_syntax.column_comparison_equality(
                bk_sink_insert, self.get_bk_snippet(tenant)
            )
        )
        if self.has_logging:
            self.artifacts.dq3_log_select.append(bk_sink_insert)
        if self.has_version:
            self._gen_bk_snippets_ver(bk_sink_insert, tenant)

    def _gen_joins_snippets(self, tenant: str | None = None) -> None:
        """Calls all join related snippet generation functions using the table tenant
        and adds snippets to the template global environment.

        Args:
            tenant (str): _description_
        """
        if not all([mapping.is_version for mapping in self.return_column_mappings]):
            self.artifacts.lu_sink_source_join.append(self.get_join_snippet(tenant))
        if self.has_logging:
            self.artifacts.dq3_log_lu_sink_source_join.append(
                self.get_join_snippet(tenant)
            )
        if self.has_version:
            for mapping in self.return_column_mappings:
                if mapping.is_version:
                    self.artifacts.versioning_artifacts[
                        mapping.table_identifier
                    ].ver_lu_sink_source_join.append(self.get_join_snippet(tenant))

    def gen(self, tenant: str | None = None) -> None:
        """Main entry method for generating all lookup snippets
        and add them to the template global environment.

        Args:
            tenant (str | None, optional): _description_. Defaults to "0".
        """
        self._gen_bk_snippets(tenant)
        self._gen_joins_snippets(tenant)
