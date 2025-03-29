import logging
import pathlib
from typing import Literal

import cloecore.utils.exceptions as custom_errors
from cloecore.utils import reader, writer
from jinja2 import Environment, PackageLoader

from cloe_extensions.crawler import crawlers, utils

logger = logging.getLogger(__name__)


def crawl(
    output_json_path: pathlib.Path,
    conn_params: dict[str, str],
    ignore_columns: bool,
    ignore_tables: bool,
    target_system_type: Literal["mssql", "snowflake", "sap"],
    existing_model_path: pathlib.Path | None = None,
    database_filter: str | None = None,
    database_name_replace: str | None = None,
    delete_old_databases: bool = False,
    sap_object_type: Literal["table", "odp"] = "odp",
    sap_tables: list[str] = [],
    sap_odp_context: str = "",
    sap_odp_objects: list[str] = [],
) -> None:
    """Crawls a snowflake instance and writes all
    metadata about database entities in a CLOE Repository JSON.

    Args:
        output_json_path (str): _description_
        snowflake_conn_params (dict): _description_. Defaults to None.
        existing_job_json_path (str | None, optional): _description_.
        Defaults to None.
        get_with_columns (bool | None, optional): _description_. Defaults to True.
    """
    crawler: crawlers.SnowflakeCrawler | crawlers.MssqlCrawler | crawlers.SapCrawler
    if target_system_type == "snowflake":
        package_loader = PackageLoader("cloe_extensions.crawler.templates", "snowflake")
        env_sql = Environment(loader=package_loader)
        crawler = crawlers.SnowflakeCrawler(
            conn_params,
            ignore_columns,
            ignore_tables,
            env_sql,
            database_filter=database_filter,
            database_name_replace=database_name_replace,
        )
    if target_system_type == "sap":
        crawler = crawlers.SapCrawler(
            conn_params,
            sap_object_type=sap_object_type,
            sap_odp_context=sap_odp_context,
            sap_odp_objects=sap_odp_objects,
            sap_tables=sap_tables,
        )
    else:
        package_loader = PackageLoader("cloe_extensions.crawler.templates", "mssql")
        env_sql = Environment(loader=package_loader)
        crawler = crawlers.MssqlCrawler(
            conn_params,
            ignore_columns,
            ignore_tables,
            env_sql,
            database_filter=database_filter,
            database_name_replace=database_name_replace,
        )
    crawler.crawl()
    databases = crawler.repository
    output_filename = "databases.json"
    if existing_model_path is not None:
        all_files = reader.find_files(existing_model_path)
        if prev_path := reader.find_model_object_path(
            all_files, "repository.db_full_catalog"
        ):
            output_filename = pathlib.Path(prev_path).name
        files_found = reader.read_models_from_disk(all_files)
        errors = custom_errors.SupportError()
        databases_old = reader.read_database_file(errors, files_found)
        errors.log_report()
        databases = utils.merge_repository_content(databases, databases_old)
        database_names = [database.name for database in databases.model_content]
        if delete_old_databases is False:
            for database in databases_old.model_content:
                if database.name not in database_names:
                    databases.model_content.append(database)
    writer.write_string_to_disk(
        databases.json(indent=4, by_alias=True, exclude_none=True),
        output_json_path / output_filename,
    )
