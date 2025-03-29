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
    "--git-tag-regex",
    required=False,
    help="Regex expressions, should lead to the last deployment tag.",
)
@click.option(
    "--func-model-filepath",
    required=True,
    type=click.Path(path_type=pathlib.Path),
    help="Relative path to functional role model YAML(from git-root-path).",
)
@click.option(
    "--func-model-previous-filepath",
    required=False,
    type=click.Path(path_type=pathlib.Path),
    help=(
        "Relative path to previous functional role model YAML(from git-root-path)."
        " Can be used if functional role model file was moved."
    ),
)
def gen_functional_roles(
    git_root_path: pathlib.Path,
    output_sql_path: pathlib.Path,
    func_model_filepath: pathlib.Path,
    git_tag_regex: str | None = None,
    func_model_previous_filepath: pathlib.Path | None = None,
) -> None:
    """Reads in a yaml describing functional roles and access to snowflake resources.
    It then generates corresponding snowflake roles and grants. In conjunction with git
    it compares last deployed yaml and current yaml to generate a change script with
    revokes/grants."""
    perm.generate_functional_roles(
        git_root_path=git_root_path,
        output_path=output_sql_path,
        func_model_filepath=func_model_filepath,
        func_model_previous_filepath=func_model_previous_filepath,
        git_tag_regex=git_tag_regex,
    )
