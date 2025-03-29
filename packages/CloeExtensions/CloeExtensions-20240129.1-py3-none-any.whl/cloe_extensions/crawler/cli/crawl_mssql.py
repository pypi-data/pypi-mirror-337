import pathlib

import click

import cloe_extensions.crawler as crawl


@click.command()
@click.argument(
    "output_json_path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "--mssql-user",
    envvar="CLOE_MSSQL_USER",
    required=True,
    help=(
        "The mssql user the crawler should use. If not set is expected"
        " as CLOE_MSSQL_USER env variable."
    ),
)
@click.option(
    "--mssql-password",
    envvar="CLOE_MSSQL_PASSWORD",
    required=True,
    help=(
        "The mssql password the crawler should use. If not set is"
        " expected as CLOE_MSSQL_PASSWORD env variable."
    ),
)
@click.option(
    "--mssql-server",
    envvar="CLOE_MSSQL_SERVER",
    required=True,
    help=(
        "The mssql server the crawler should use. If not set is expected"
        " as CLOE_MSSQL_SERVER env variable."
    ),
)
@click.option(
    "--mssql-database",
    envvar="CLOE_MSSQL_DATABASE",
    required=True,
    help=(
        "The mssql database the crawler should use. If not set is expected"
        " as CLOE_MSSQL_DATABASE env variable."
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
        "Filters databases based on defined filter. Is used as Mssql wildcard"
        " pattern in SYS.DATABASES. If no filter defined all databases are retrieved."
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
def crawl_mssql(
    output_json_path: pathlib.Path,
    mssql_user: str,
    mssql_password: str,
    mssql_server: str,
    mssql_database: str,
    ignore_columns: bool,
    ignore_tables: bool,
    existing_model_path: pathlib.Path | None = None,
    database_filter: str | None = None,
    database_name_replace: str | None = None,
    delete_old_databases: bool = False,
) -> None:
    """This script crawls a mssql database and returns the
    information schema in a CLOE compatible json format."""
    mssql_conn_params = {
        "UID": mssql_user,
        "PWD": mssql_password,
        "SERVER": mssql_server,
        "DATABASE": mssql_database,
    }
    crawl.crawl(
        output_json_path,
        mssql_conn_params,
        ignore_columns,
        ignore_tables,
        "mssql",
        existing_model_path,
        database_filter,
        database_name_replace,
        delete_old_databases,
    )
