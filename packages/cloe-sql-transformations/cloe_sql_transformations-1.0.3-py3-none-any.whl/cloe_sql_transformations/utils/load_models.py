import pathlib

from cloe_metadata import base
from cloe_metadata.shared.modeler import power_pipe, simple_pipe
from cloe_metadata.utils import model_transformer


def load_models(
    input_model_path: pathlib.Path,
) -> tuple[
    list[power_pipe.PowerPipe],
    list[simple_pipe.SimplePipe],
    base.SQLTemplates,
    base.ConversionTemplates,
]:
    pipes, p_errors = base.Pipes.read_instances_from_disk(input_model_path)
    databases, d_errors = base.Databases.read_instances_from_disk(input_model_path)
    tenants, t_errors = base.Tenants.read_instances_from_disk(input_model_path)
    conversion_templates, c_errors = base.ConversionTemplates.read_instances_from_disk(
        input_model_path
    )
    sql_templates, sql_errors = base.SQLTemplates.read_instances_from_disk(
        input_model_path
    )
    trans_power_pipes, t_pp_errors = model_transformer.transform_power_pipes_to_shared(
        base_obj_collection=pipes,
        databases=databases,
        tenants=tenants,
        conversion_templates=conversion_templates,
        sql_templates=sql_templates,
    )
    (
        trans_simple_pipes,
        t_sp_errors,
    ) = model_transformer.transform_simple_pipes_to_shared(
        base_obj_collection=pipes,
        databases=databases,
    )
    if (
        len(p_errors) > 0
        or len(d_errors) > 0
        or len(c_errors) > 0
        or len(t_errors) > 0
        or len(sql_errors) > 0
        or len(t_pp_errors) > 0
        or len(t_sp_errors) > 0
    ):
        raise ValueError(
            "The provided models did not pass validation, please run validation.",
        )

    return (trans_power_pipes, trans_simple_pipes, sql_templates, conversion_templates)
