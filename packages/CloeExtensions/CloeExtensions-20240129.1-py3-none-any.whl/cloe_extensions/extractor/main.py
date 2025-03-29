import pathlib

from cloecore.utils import reader, writer

from cloe_extensions.extractor.db2fs_fs2db_generator import (
    GeneratorParams,
    filter_catalogs,
    generate_dataset_db2fs_fs2db,
)


def db2fs_fs2db(
    input_json_file_path: pathlib.Path,
    output_json_folder_path: pathlib.Path,
    job_catalog_filter_positive: str | None = None,
    job_catalog_filter_negative: str | None = None,
    output_dataset_json_file_name_ending: str = "_dataset",
    output_db2fs_json_file_name_ending: str = "_db2fs",
    output_fs2db_json_file_name_ending: str = "_fs2db",
    dataset_type: str = "Parquet",
) -> None:
    """
    Generates a datasettype.json, a db2fs.json, and a fs2db.json from an input db model
    with optional catalog filters.
    """

    input_json_file_name = input_json_file_path.name

    input_model = reader.read_json_from_disk(input_json_file_path)

    generator_params = GeneratorParams(dataset_type=dataset_type)

    if job_catalog_filter_positive or job_catalog_filter_negative:
        input_model[generator_params.json_key_database_content] = filter_catalogs(
            input_model[generator_params.json_key_database_content],
            job_catalog_filter_positive,
            job_catalog_filter_negative,
        )

    dataset_prep_dict, db2fs_prep_dict, fs2db_prep_dict = generate_dataset_db2fs_fs2db(
        input_model, generator_params
    )

    output_dataset_json_file_name = (
        f"{input_json_file_name.split('.')[0]}{output_dataset_json_file_name_ending}"
        f".{input_json_file_name.split('.')[1]}"
    )
    output_db2fs_json_file_name = (
        f"{input_json_file_name.split('.')[0]}{output_db2fs_json_file_name_ending}"
        f".{input_json_file_name.split('.')[1]}"
    )
    output_fs2db_json_file_name = (
        f"{input_json_file_name.split('.')[0]}{output_fs2db_json_file_name_ending}"
        f".{input_json_file_name.split('.')[1]}"
    )

    writer.write_dict_to_disk_json(
        dataset_prep_dict, output_json_folder_path / output_dataset_json_file_name
    )
    writer.write_dict_to_disk_json(
        db2fs_prep_dict, output_json_folder_path / output_db2fs_json_file_name
    )
    writer.write_dict_to_disk_json(
        fs2db_prep_dict, output_json_folder_path / output_fs2db_json_file_name
    )
