import pathlib

import cloecore.to_sql.model.modeler as tmodeler
import cloecore.utils.writer as writer
from cloecore.to_sql.model import modeler


def deploy_dq_views(
    pipes: list[tmodeler.SimplePipeGenerator | tmodeler.PowerPipeGenerator],
    output_path: pathlib.Path,
    output_sql_transaction_separator: str,
) -> None:
    dq_views: dict[str, str] = {}
    for pipe in pipes:
        if isinstance(pipe, modeler.PowerPipeGenerator):
            dq_views |= pipe.gen_dq_views(output_sql_transaction_separator)
    complete_file = ""
    for dq_key, out in dq_views.items():
        complete_file += f"\n\n\n\n--NEXT Table STARTING {dq_key}\n{out}"
    writer.write_string_to_disk(complete_file, output_path / "dq_view_ddls.sql")
