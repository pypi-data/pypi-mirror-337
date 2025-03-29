import pathlib
from pathlib import PurePath

from cloecore.utils import writer

from cloe_extensions.converter.converter import (
    ConverterParams,
    fill_databasetables,
    prep_dict_from_databasetables,
    read_csv_from_disk,
    replace_string_for_null_with_none,
)


def convert(
    csv_file_path: pathlib.Path,
    json_folder_path: pathlib.Path,
    catalogs_column_name: str,
    schemas_column_name: str,
    tables_column_name: str,
    columns_column_name: str,
    ordinal_positions_column_name: str,
    data_types_column_name: str,
    csv_delimiter: str,
    csv_encoding: str,
    data_type_precisions_column_name: str | None = None,
    datetime_precisions_column_name: str | None = None,
    string_value_for_null: str
    | None = None,  # must be defined if datetime_precisions_column_name was defined
    data_type_lengths_column_name: str | None = None,
    data_type_numeric_scales_column_name: str | None = None,
    is_key_column_name: bool | None = None,
    is_nullable_column_name: bool | None = None,
    constraints_column_name: str | None = None,
) -> None:
    """
    Converts information_schema CSV to a JSON with information about databases,
    schemas, tables, and columns.
    """
    converter_params = ConverterParams(
        csv_file_path=csv_file_path,
        json_folder_path=json_folder_path,
        csv_delimiter=csv_delimiter,
        csv_encoding=csv_encoding,
        catalogs_column_name=catalogs_column_name,
        schemas_column_name=schemas_column_name,
        tables_column_name=tables_column_name,
        columns_column_name=columns_column_name,
        ordinal_positions_column_name=ordinal_positions_column_name,
        data_types_column_name=data_types_column_name,
        data_type_precisions_column_name=data_type_precisions_column_name,
        datetime_precisions_column_name=datetime_precisions_column_name,
        data_type_lengths_column_name=data_type_lengths_column_name,
        data_type_numeric_scales_column_name=data_type_numeric_scales_column_name,
        is_key_column_name=is_key_column_name,
        is_nullable_column_name=is_nullable_column_name,
        constraints_column_name=constraints_column_name,
    )
    csv_dicts = read_csv_from_disk(
        file_path=converter_params.csv_file_path,
        headers_tf=True,
        delimiter=converter_params.csv_delimiter,
        encoding=converter_params.csv_encoding,
    )
    if string_value_for_null:
        csv_dicts = replace_string_for_null_with_none(csv_dicts, string_value_for_null)
    databasetables = fill_databasetables(csv_dicts, converter_params)
    prep_dict = prep_dict_from_databasetables(databasetables, converter_params)
    json_file_name = (
        f"{PurePath(converter_params.csv_file_path).parts[1].split('.')[0]}.json"
    )
    writer.write_dict_to_disk_json(
        prep_dict, converter_params.json_folder_path / json_file_name
    )
