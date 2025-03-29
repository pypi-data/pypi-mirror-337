from typing import Generator


def update_values_in_nested_dict(
    nested_dict, key_to_be_mapped: str, mapping: dict
) -> Generator:
    if key_to_be_mapped in nested_dict:
        nested_dict[key_to_be_mapped] = mapping[nested_dict[key_to_be_mapped].upper()]
        yield nested_dict[key_to_be_mapped]
    for k in nested_dict:
        if isinstance(nested_dict[k], list):
            for i in nested_dict[k]:
                for j in update_values_in_nested_dict(i, key_to_be_mapped, mapping):
                    yield j


def transform_sql_sever_to_snf(source_model: dict) -> dict:
    """
    Transforms a source database dict to a snowflake database dict.
    """
    data_type_mapping = {
        # Numerics
        "INT": "INT",
        "BIGINT": "INT",
        "SMALLINT": "INT",
        "TINYINT": "INT",
        "NUMERIC": "NUMBER",
        "DECIMAL": "FLOAT",
        "SMALLMONEY": "FLOAT",
        "MONEY": "FLOAT",
        "BIT": "",  # missing (INT or BOOLEAN)?
        "FLOAT": "FLOAT",
        "REAL": "FLOAT",
        # Date And Time
        "DATE": "DATE",
        "DATETIMEOFFSET": "TIMESTAMP_TZ",
        "DATETIME2": "TIMESTAMP_NTZ",
        "SMALLDATETIME": "TIMESTAMP_NTZ",
        "DATETIME": "TIMESTAMP_NTZ",
        "TIME": "TIME",
        # Character Strings
        "CHAR": "VARCHAR",
        "VARCHAR": "VARCHAR",
        "TEXT": "VARCHAR",
        "NCHAR": "VARCHAR",
        "NVARCHAR": "VARCHAR",
        "NTEXT": "VARCHAR",
        # Binary Strings
        "BINARY": "BINARY",
        "VARBINARY": "BINARY",
        "IMAGE": "",  # not supported
    }
    for source_database in source_model["modelContent"]:
        list(
            update_values_in_nested_dict(source_database, "DataType", data_type_mapping)
        )
    snowflake_model = source_model
    return snowflake_model
