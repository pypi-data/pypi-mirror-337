import jinja2
from cloe_metadata import base
from cloe_metadata.shared.modeler import power_pipe, simple_pipe

from cloe_sql_transformations.model import (
    ConversionTemplateGenerator,
    PowerPipeGenerator,
    SimplePipeGenerator,
)
from cloe_sql_transformations.model.sql_syntax import SQLSyntax


def transform_pipes(
    power_pipes: list[power_pipe.PowerPipe],
    simple_pipes: list[simple_pipe.SimplePipe],
    sql_syntax: SQLSyntax,
    object_identifier_template: jinja2.Template,
) -> list[PowerPipeGenerator | SimplePipeGenerator]:
    """
    Transform power_pipes and simple_pipes to custom classes.
    """
    trans_pipes: list[PowerPipeGenerator | SimplePipeGenerator] = []
    for shared_power_pipe in power_pipes:
        trans_pipes.append(
            PowerPipeGenerator(
                shared_power_pipe,
                sql_syntax,
                object_identifier_template=object_identifier_template,
            )
        )
    for shared_simple_pipe in simple_pipes:
        trans_pipes.append(
            SimplePipeGenerator(
                shared_simple_pipe,
                object_identifier_template=object_identifier_template,
            )
        )
    return trans_pipes


def transform_common(
    conversion_templates: base.ConversionTemplates, sql_syntax: SQLSyntax
) -> dict[str, ConversionTemplateGenerator]:
    """Transforms common templates."""
    converted_conversions: dict[str, ConversionTemplateGenerator] = {}
    for k, temp in conversion_templates.get_templates().items():
        if isinstance(temp, base.ConversionTemplate):
            converted_conversions[k] = ConversionTemplateGenerator(temp, sql_syntax)
    return converted_conversions
