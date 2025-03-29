import pathlib

import click

import cloe_extensions.snowflake_access_control as perm


@click.command()
@click.argument(
    "input_sql_path",
    type=click.Path(exists=True, resolve_path=True, path_type=pathlib.Path),
)
@click.option(
    "--snowflake-user",
    envvar="CLOE_SNOWFLAKE_USER",
    required=True,
    help=(
        "The snowflake user the crawler should use. If not set is expected"
        " as CLOE_SNOWFLAKE_USER env variable."
    ),
)
@click.option(
    "--snowflake-password",
    envvar="CLOE_SNOWFLAKE_PASSWORD",
    required=True,
    help=(
        "The snowflake password the crawler should use. If not set is"
        " expected as CLOE_SNOWFLAKE_PASSWORD env variable."
    ),
)
@click.option(
    "--snowflake-account",
    envvar="CLOE_SNOWFLAKE_ACCOUNT",
    required=True,
    help=(
        "The snowflake account the crawler should use. If not set is expected"
        " as CLOE_SNOWFLAKE_ACCOUNT env variable."
    ),
)
@click.option(
    "--snowflake-warehouse",
    envvar="CLOE_SNOWFLAKE_WAREHOUSE",
    required=True,
    help=(
        "The snowflake warehouse the crawler should use. If not set is"
        " expected as CLOE_SNOWFLAKE_WAREHOUSE env variable."
    ),
)
@click.option(
    "--fail-on-sql-error",
    default=False,
    is_flag=True,
    help="Fail/stop if one of the queries causes an error.",
)
@click.option(
    "--snowflake-role",
    envvar="CLOE_SNOWFLAKE_ROLE",
    required=False,
    help=(
        "The snowflake role the crawler should use. Can also be set with"
        " the CLOE_SNOWFLAKE_ROLE env variable. If not set uses users default role."
    ),
)
def deploy_roles(
    input_sql_path: pathlib.Path,
    snowflake_user: str,
    snowflake_password: str,
    snowflake_account: str,
    snowflake_warehouse: str,
    fail_on_sql_error: bool,
    snowflake_role: str | None = None,
) -> None:
    """This script takes in an sql script and executes
    it on a snowflake instance."""
    snowflake_conn_params = {
        "user": snowflake_user,
        "password": snowflake_password,
        "account": snowflake_account,
        "warehouse": snowflake_warehouse,
    }
    if snowflake_role is not None:
        snowflake_conn_params["role"] = snowflake_role
    perm.deploy(
        input_sql_path, snowflake_conn_params, continue_on_error=not fail_on_sql_error
    )
