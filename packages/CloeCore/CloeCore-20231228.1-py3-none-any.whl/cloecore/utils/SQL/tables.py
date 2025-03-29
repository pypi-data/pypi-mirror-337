from cloecore.utils.templating_engine.general_templates import env


def insert_table_sql(
    rows: list[dict],
    schema_name: str,
    table_name: str,
    output_sql_transaction_separator: str | None = None,
    truncate_before_insert: bool = False,
    identity_insert: bool = False,
) -> str:
    if len(rows) == 0:
        return ""
    template = env.get_template("insert_table.sql.j2")
    sink_columns = list(rows[0].keys())
    insert_values_list = [[row[key] for key in sink_columns] for row in rows]
    insert_query = template.render(
        identity_insert=identity_insert,
        truncate_before_insert=truncate_before_insert,
        schema_name=schema_name,
        table_name=table_name,
        sink_columns=sink_columns,
        insert_values_list=insert_values_list,
        output_sql_transaction_separator=output_sql_transaction_separator,
    )
    return insert_query
