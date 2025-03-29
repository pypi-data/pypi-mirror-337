import pathlib

import click

import cloe_extensions.database_transformation as transform


@click.command()
@click.argument(
    "input-json-file-path",
    type=click.Path(
        exists=True, resolve_path=True, writable=True, path_type=pathlib.Path
    ),
)
@click.argument(
    "output-json-folder-path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "--output-json-file-name-ending",
    default="_snf",
    show_default=True,
    help=(
        "The suffix of the output json file name is by default _snf "
        "and can be re-defined here."
    ),
)
def transform_db_model_to_snowflake(
    input_json_file_path: pathlib.Path,
    output_json_folder_path: pathlib.Path,
    output_json_file_name_ending: str,
) -> None:
    """
    Transforms a source database JSON to a snowflake database JSON.
    """
    transform.transform(
        input_json_file_path=input_json_file_path,
        output_json_folder_path=output_json_folder_path,
        output_json_file_name_ending=output_json_file_name_ending,
    )
