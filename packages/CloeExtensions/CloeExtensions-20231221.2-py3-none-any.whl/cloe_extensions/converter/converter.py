import csv
import pathlib
import uuid
from dataclasses import dataclass

from cloe_extensions.utils.model.database import DatabaseTable


@dataclass
class ConverterParams:
    """
    All parameters for the CSV to JSON converter are centrally defined for
    better overview.
    """

    csv_file_path: pathlib.Path
    json_folder_path: pathlib.Path
    csv_delimiter: str
    csv_encoding: str
    catalogs_column_name: str
    schemas_column_name: str
    tables_column_name: str
    columns_column_name: str
    ordinal_positions_column_name: str
    data_types_column_name: str
    data_type_precisions_column_name: str | None = None
    datetime_precisions_column_name: str | None = None
    data_type_lengths_column_name: str | None = None
    data_type_numeric_scales_column_name: str | None = None
    is_key_column_name: bool | None = None
    is_nullable_column_name: bool | None = None
    constraints_column_name: str | None = None
    json_key_database_model_id: str = "modelID"
    json_database_model_id: str = "repository.db_full_catalog"
    json_key_database_content: str = "modelContent"
    json_key_database_name: str = "name"
    json_key_schema_content: str = "schemas"
    json_key_schema_name: str = "name"
    json_key_table_level: str = "tables"


def read_csv_from_disk(
    file_path: pathlib.Path, headers_tf: bool, delimiter: str, encoding: str
) -> list:
    """
    Returns a list of dictionaries which represent the rows of a csv.
    """
    with open(file_path, newline="", encoding=encoding) as csvfile:
        csv_dicts = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(
                csvfile, skipinitialspace=headers_tf, delimiter=delimiter
            )
        ]
    return csv_dicts


def replace_string_for_null_with_none(
    dicts_with_string_for_null: list[dict], string_value_for_null: str
) -> list[dict]:
    """
    Replaces all string values for null with none in a list of dictionaries.
    """
    for dict_with_string_for_null in dicts_with_string_for_null:
        for k, v in dict_with_string_for_null.items():
            if v == string_value_for_null:
                dict_with_string_for_null[k] = None
    return dicts_with_string_for_null


def fill_databasetables(
    csv_dicts: list[dict], converter_params: ConverterParams
) -> list[DatabaseTable]:
    """
    Iterates over all tables in the CSV. Initializes DatabaseTable class for each table
    and concatenates them to a databasetables list.
    """
    databasetables = []
    my_tables = {}
    for row in csv_dicts:
        table_ident = (
            f"{row[converter_params.catalogs_column_name]}"
            f".{row[converter_params.schemas_column_name]}"
            f".{row[converter_params.tables_column_name]}"
        )
        if table_ident not in my_tables:
            my_tables[table_ident] = [row]
        else:
            my_tables[table_ident].append(row)

    for table_ident, table_columns in my_tables.items():
        table_idents = table_ident.split(".")
        new_table = DatabaseTable(
            id=uuid.uuid4(),
            schema_name=table_idents[1],
            name=table_idents[2],
        )
        new_table.add_columns(table_columns, converter_params)
        databasetables.append(new_table)
    return databasetables


# def database_prepare(
#     databasetable: DatabaseTable,
#     database_content: list[dict],
#     converter_params: ConverterParams,
# ) -> tuple[list[dict], list[dict]]:
#     if databasetable.catalog_name not in [
#         database[converter_params.json_key_database_name]
#         for database in database_content
#     ]:
#         database_schemas: list[dict] = []
#         database_content.append(
#             {
#                 converter_params.json_key_database_name: databasetable.catalog_name,
#                 converter_params.json_key_schema_content: database_schemas,
#             }
#         )
#     else:
#         for database in database_content:
#             if (
#                 database[converter_params.json_key_database_name]
#                 == databasetable.catalog_name
#             ):
#                 database_schemas = database[converter_params.json_key_schema_content]
#     return database_content, database_schemas


def schema_prepare(
    databasetable: DatabaseTable,
    database_schemas: list[dict],
    converter_params: ConverterParams,
) -> tuple[list[dict], list[dict]]:
    if databasetable.schema_name not in [
        schema[converter_params.json_key_schema_name] for schema in database_schemas
    ]:
        schema_tables: list[dict] = []
        database_schemas.append(
            {
                converter_params.json_key_schema_name: databasetable.schema_name,
                converter_params.json_key_table_level: schema_tables,
            }
        )
    else:
        for schema in database_schemas:
            if (
                schema[converter_params.json_key_schema_name]
                == databasetable.schema_name
            ):
                schema_tables = schema[converter_params.json_key_table_level]
    return database_schemas, schema_tables


def prep_dict_from_databasetables(
    databasetables: list[DatabaseTable], converter_params: ConverterParams
) -> dict:
    """
    Iterates over all databasetables to prepare a dictionary
    for write_dict_to_disk_json.
    """
    # json_key_database_model_id = converter_params.json_key_database_model_id
    # database_content: list[dict] = []
    # prep_dict = {
    #     json_key_database_model_id: converter_params.json_database_model_id,
    #     converter_params.json_key_database_content: database_content,
    # }
    # for databasetable in databasetables:
    #     database_content, database_schemas = database_prepare(
    #         databasetable, database_content, converter_params
    #     )
    #     database_schemas, schema_tables = schema_prepare(
    #         databasetable, database_schemas, converter_params
    #     )
    #     databasetable_prep_dict, catalog_name, schema_name = databasetable.json()
    #     schema_tables.append(databasetable_prep_dict)
    return {"function": "needs maintenance"}
