import pathlib

from cloecore.utils import reader, writer

from cloe_extensions.database_transformation.transformer import (
    transform_sql_sever_to_snf,
)


def transform(
    input_json_file_path: pathlib.Path,
    output_json_folder_path: pathlib.Path,
    output_json_file_name_ending: str,
) -> None:
    """
    Transforms a source database JSON to a snowflake database JSON.
    """
    source_model = reader.read_json_from_disk(input_json_file_path)
    input_json_file_name = input_json_file_path.name
    snowflake_model = transform_sql_sever_to_snf(source_model)
    output_json_file_name = (
        f"{input_json_file_name.split('.')[0]}{output_json_file_name_ending}."
        f"{input_json_file_name.split('.')[1]}"
    )
    writer.write_dict_to_disk_json(
        snowflake_model, output_json_folder_path / output_json_file_name
    )
