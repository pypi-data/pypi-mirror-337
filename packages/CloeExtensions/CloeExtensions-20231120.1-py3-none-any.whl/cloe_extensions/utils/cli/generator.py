import click

import cloe_extensions.converter.cli as converter_cli
import cloe_extensions.database_transformation.cli as transdb_cli
import cloe_extensions.snowflake_access_control.cli as snow_cli


@click.group()
def generator_cli():
    """Endpoint to register new CLI commands.
    should be used by all extension CLIs having
    a generator like purpose.
    """
    pass


generator_cli.add_command(snow_cli.gen_technical_roles)
generator_cli.add_command(snow_cli.gen_functional_roles)
generator_cli.add_command(converter_cli.convert_csv_to_db_model)
generator_cli.add_command(transdb_cli.transform_db_model_to_snowflake)
