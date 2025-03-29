import pathlib

import click

import cloe_extensions.crawler as crawl


@click.command()
@click.argument(
    "output_json_path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
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
    "--snowflake-role",
    envvar="CLOE_SNOWFLAKE_ROLE",
    required=False,
    help=(
        "The snowflake role the crawler should use. Can also be set with"
        " the CLOE_SNOWFLAKE_ROLE env variable. If not set uses users default role."
    ),
)
@click.option(
    "--existing-model-path",
    required=False,
    type=click.Path(
        exists=True, resolve_path=True, writable=True, path_type=pathlib.Path
    ),
    help="Reference an existing Repository json to update.",
)
@click.option(
    "--ignore-columns",
    is_flag=True,
    show_default=True,
    default=False,
    help=(
        "Ignore columns of tables and just retrieve information"
        " about the table itself."
    ),
)
@click.option(
    "--ignore-tables",
    is_flag=True,
    show_default=True,
    default=False,
    help=(
        "Ignore tables and just retrieve information about the higher level objects."
    ),
)
@click.option(
    "--database-filter",
    required=False,
    help=(
        "Filters databases based on defined filter. Is used as Snowflake wildcard"
        " pattern in SHOW DATABASES. If no filter defined all databases are retrieved."
    ),
)
@click.option(
    "--database-name-replace",
    required=False,
    help=(
        "Replaces parts of a name with the CLOE env placeholder. Can be regex. Can be"
        " used to remove the environment part in a database name."
    ),
)
@click.option(
    "--delete-old-databases",
    is_flag=True,
    show_default=True,
    default=False,
    help=("Delete old databases if do not exist in target."),
)
def crawl_snowflake(
    output_json_path: pathlib.Path,
    snowflake_user: str,
    snowflake_password: str,
    snowflake_account: str,
    snowflake_warehouse: str,
    ignore_columns: bool,
    ignore_tables: bool,
    snowflake_role: str | None = None,
    existing_model_path: pathlib.Path | None = None,
    database_filter: str | None = None,
    database_name_replace: str | None = None,
    delete_old_databases: bool = False,
) -> None:
    """This script crawls a snowflake database and returns the
    information schema in a CLOE compatible json format."""
    snowflake_conn_params = {
        "user": snowflake_user,
        "password": snowflake_password,
        "account": snowflake_account,
        "warehouse": snowflake_warehouse,
    }
    if snowflake_role is not None:
        snowflake_conn_params["role"] = snowflake_role
    crawl.crawl(
        output_json_path,
        snowflake_conn_params,
        ignore_columns,
        ignore_tables,
        "snowflake",
        existing_model_path,
        database_filter,
        database_name_replace,
        delete_old_databases,
    )
