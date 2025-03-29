import pathlib

import click

import cloe_extensions.converter as convert


@click.command()
@click.argument(
    "csv-file-path",
    type=click.Path(
        exists=True, resolve_path=True, writable=True, path_type=pathlib.Path
    ),
)
@click.argument(
    "json-folder-path",
    type=click.Path(
        exists=True, resolve_path=True, writable=True, path_type=pathlib.Path
    ),
)
@click.option(
    "--catalogs-column-name",
    default="TABLE_CATALOG",
    show_default=True,
    help="Catalogs column name if it deviates from 'TABLE_CATALOG'.",
)
@click.option(
    "--schemas-column-name",
    default="TABLE_SCHEMA",
    show_default=True,
    help="Schemas column name if it deviates from 'TABLE_SCHEMA'.",
)
@click.option(
    "--tables-column-name",
    default="TABLE_NAME",
    show_default=True,
    help="Tables column name if it deviates from 'TABLE_NAME'.",
)
@click.option(
    "--columns-column-name",
    default="COLUMN_NAME",
    show_default=True,
    help="Columns column name if it deviates from 'COLUMN_NAME'.",
)
@click.option(
    "--ordinal-positions-column-name",
    default="ORDINAL_POSITION",
    show_default=True,
    help="Ordinal column name if it deviates from 'ORDINAL_POSITION'.",
)
@click.option(
    "--data-types-column-name",
    default="DATA_TYPE",
    show_default=True,
    help="Data column name if it deviates from 'DATA_TYPE'.",
)
@click.option(
    "--csv-delimiter",
    default=";",
    show_default=True,
    help="CSV delimiter if it deviates from ';'.",
)
@click.option(
    "--csv-encoding",
    default="utf-8-sig",
    show_default=True,
    help="CSV encoding if it deviates from 'utf-8-sig'.",
)
@click.option(
    "--data-type-precisions-column-name",
    required=False,
    help="CSV-column name of the data type precisions.",
)
@click.option(
    "--datetime-precisions-column-name",
    required=False,
    help=(
        "CSV-column name of the datetime precisions. Please also define"
        " the string-value-for-null if this optional parameter is defined."
    ),
)
@click.option(
    "--string-value-for-null",
    required=False,
    help=(
        "The string value that represents null (no data) in the CSV-File."
        " Must be defined if datetime-precisions-column-name was defined"
    ),
)
@click.option(
    "--data-type-lengths-column-name",
    required=False,
    help="CSV-column name of the data type lengths.",
)
@click.option(
    "--data-type-numeric-scales-column-name",
    required=False,
    help="CSV-column name of the data type numeric scales.",
)
@click.option(
    "--is-key-column-name",
    required=False,
    help="IsKey-column name.",
)
@click.option(
    "--is-nullable-column-name",
    required=False,
    help="IsNullable-column name.",
)
@click.option(
    "--constraints-column-name",
    required=False,
    help="Constraints-column name.",
)
def convert_csv_to_db_model(
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
    data_type_precisions_column_name: str | None,
    datetime_precisions_column_name: str | None,
    string_value_for_null: str | None,
    data_type_lengths_column_name: str | None,
    data_type_numeric_scales_column_name: str | None,
    is_key_column_name: bool | None,
    is_nullable_column_name: bool | None,
    constraints_column_name: str | None,
) -> None:
    """
    Convert an information_schema CSV to a db_model JSON.
    """
    convert.convert(
        csv_file_path=csv_file_path,
        json_folder_path=json_folder_path,
        catalogs_column_name=catalogs_column_name,
        schemas_column_name=schemas_column_name,
        tables_column_name=tables_column_name,
        columns_column_name=columns_column_name,
        ordinal_positions_column_name=ordinal_positions_column_name,
        data_types_column_name=data_types_column_name,
        csv_delimiter=csv_delimiter,
        csv_encoding=csv_encoding,
        data_type_precisions_column_name=data_type_precisions_column_name,
        datetime_precisions_column_name=datetime_precisions_column_name,
        string_value_for_null=string_value_for_null,
        data_type_lengths_column_name=data_type_lengths_column_name,
        data_type_numeric_scales_column_name=data_type_numeric_scales_column_name,
        is_key_column_name=is_key_column_name,
        is_nullable_column_name=is_nullable_column_name,
        constraints_column_name=constraints_column_name,
    )
