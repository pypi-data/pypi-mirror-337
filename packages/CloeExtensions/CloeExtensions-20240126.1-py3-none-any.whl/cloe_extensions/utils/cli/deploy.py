import click

import cloe_extensions.snowflake_access_control.cli as snow_cli


@click.group()
def deploy_cli():
    """Endpoint to register new CLI commands.
    should be used by all extension CLIs having
    a deploy like purpose.
    """
    pass


deploy_cli.add_command(snow_cli.deploy_roles)
