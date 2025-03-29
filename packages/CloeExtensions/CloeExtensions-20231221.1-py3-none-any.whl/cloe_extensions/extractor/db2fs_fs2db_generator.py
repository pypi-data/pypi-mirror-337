import re
import uuid
from dataclasses import dataclass
from typing import cast


@dataclass
class GeneratorParams:
    """
    All parameters for the db2fs_fs2db generator are centrally defined for better
    overview.
    """

    dataset_type: str  # input parameter
    json_key_database_content: str = "modelContent"
    json_key_database_name: str = "name"
    json_key_schema_content: str = "schemas"
    json_key_schema_name: str = "name"
    json_key_table_level: str = "tables"
    json_key_table_name: str = "name"
    json_key_columns: str = "columns"
    string_value_for_null: str = "NULL"


def filter_catalogs(
    model_content: list[dict],
    job_catalog_filter_positive: str | None = None,
    job_catalog_filter_negative: str | None = None,
) -> list[dict]:
    filtered_content = []
    for catalog in model_content:
        if (
            not job_catalog_filter_positive
            or re.match(job_catalog_filter_positive, catalog["name"])
        ) and (
            not job_catalog_filter_negative
            or not re.match(job_catalog_filter_negative, catalog["name"])
        ):
            filtered_content.append(catalog)
    return filtered_content


def generate_dataset_db2fs_fs2db(
    input_model: dict, generator_params: GeneratorParams
) -> tuple[dict, dict, dict]:
    """
    Prepares dictionaries for a datasettype.json, a db2fs.json, and a fs2db.json from
    an input db model.
    """
    model_id_key = "modelID"
    dataset_prep_dict = {model_id_key: "repository.ds_datasettype", "modelContent": []}
    db2fs_prep_dict = {model_id_key: "jobs.db2fs", "modelContent": []}
    fs2db_prep_dict = {model_id_key: "jobs.fs2db", "modelContent": []}

    databases = input_model[generator_params.json_key_database_content]
    for database in databases:
        database_name = database[generator_params.json_key_database_name]
        schemas = database[generator_params.json_key_schema_content]
        for schema in schemas:
            schema_name = schema[generator_params.json_key_schema_name]
            tables = schema[generator_params.json_key_table_level]
            for table in tables:
                table_name = table[generator_params.json_key_table_name]
                columns = table[generator_params.json_key_columns]
                ds_attributes: list[dict[str, str]] = []
                dataset: dict[str, list | str] = {
                    "attributes": ds_attributes,
                    "id": str(uuid.uuid4()),
                    "name": f"DST_{schema_name}_{table_name}",
                    "storage_format": generator_params.dataset_type,
                }
                for column in columns:
                    attribute = {"datatype": column["dataType"], "name": column["name"]}
                    ds_attributes.append(attribute)
                db2fs_job = {
                    "datasetTypeID": dataset["id"],
                    "sourcetableID": table_name,
                    "folderPath": database_name + "/" + schema_name + "/" + table_name,
                    "sourceSelectStatement": "SELECT * FROM {{ source_table }}",
                    "id": str(uuid.uuid4()),
                    "name": f"Extract {table_name} FULL",
                }
                fs2db_job = {
                    "getFromFileCatalog": True,
                    "sinkTableID": table["ID"],
                    "id": str(uuid.uuid4()),
                    "name": f"Load {table_name}",
                }
                cast(list, dataset_prep_dict["modelContent"]).append(dataset)
                cast(list, db2fs_prep_dict["modelContent"]).append(db2fs_job)
                cast(list, fs2db_prep_dict["modelContent"]).append(fs2db_job)

    return dataset_prep_dict, db2fs_prep_dict, fs2db_prep_dict
