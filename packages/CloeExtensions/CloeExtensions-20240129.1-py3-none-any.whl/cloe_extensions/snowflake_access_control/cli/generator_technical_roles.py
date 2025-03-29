import pathlib

import click

import cloe_extensions.snowflake_access_control as perm


@click.command()
@click.argument(
    "git-root-path",
    type=click.Path(exists=True, resolve_path=True, path_type=pathlib.Path),
)
@click.argument(
    "output-sql-path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "--database-filter-positive",
    required=False,
    help="Regex expressions, use databases matched by the expression.",
)
@click.option(
    "--database-filter-negative",
    required=False,
    help="Regex expressions, exclude databases matched by the expression.",
)
@click.option(
    "--git-tag-regex",
    required=False,
    help="Regex expressions, should lead to the last deployment tag.",
)
@click.option(
    "--database-model-filepath",
    required=True,
    type=click.Path(path_type=pathlib.Path),
    help="Relative path to database model file (from git-root-path).",
)
@click.option(
    "--database-model-previous-filepath",
    required=False,
    type=click.Path(path_type=pathlib.Path),
    help=(
        "Relative path to previous database model file (from git-root-path)."
        " Can be used if database model file was moved."
    ),
)
@click.option(
    "--use-incremental-mode",
    show_default=True,
    default=False,
    is_flag=True,
    help="Use incremental mode to only create roles and grants for new objects.",
)
def gen_technical_roles(
    git_root_path: pathlib.Path,
    output_sql_path: pathlib.Path,
    database_model_filepath: pathlib.Path,
    database_filter_positive: str | None,
    database_filter_negative: str | None,
    git_tag_regex: str | None = None,
    database_model_previous_filepath: pathlib.Path | None = None,
    use_incremental_mode: bool = False,
) -> None:
    """This script reads in a json describing the database and
    filters object based on defined filters. It then generates all
    necessary snowflake roles."""
    perm.generate_technical_roles(
        git_root_path=git_root_path,
        output_path=output_sql_path,
        database_model_filepath=database_model_filepath,
        database_model_previous_filepath=database_model_previous_filepath,
        git_tag_regex=git_tag_regex,
        database_filter_positive=database_filter_positive,
        database_filter_negative=database_filter_negative,
        use_incremental_mode=use_incremental_mode,
    )
