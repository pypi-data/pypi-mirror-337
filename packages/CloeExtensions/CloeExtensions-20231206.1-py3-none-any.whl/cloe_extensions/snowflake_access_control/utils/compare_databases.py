import logging

import cloecore.utils.model.repository.database as model_db

logger = logging.getLogger(__name__)


def find_deleted_schemas_in_databases(
    database_old: model_db.DatabaseDatabase,
    database_new: model_db.DatabaseDatabase | None = None,
) -> list[str]:
    """Comparing two databases and return list of schemas not existing in
    new database.

    Args:
        database_old (dict): _description_
        database_new (dict): _description_

    Returns:
        list: _description_
    """
    if database_new is None:
        return [schema.name for schema in database_old.schemas]
    deleted_schemas: list[str] = []
    existing_schemas = [schema.name for schema in database_new.schemas]
    for schema in database_old.schemas:
        if schema.name not in existing_schemas:
            deleted_schemas.append(schema.name)
            logger.info(
                "Schema %s in database %s deleted.",
                schema.name,
                database_old.name,
            )
    return deleted_schemas


def find_deleted_databases(
    databases_old: list[model_db.DatabaseDatabase],
    databases_new: list[model_db.DatabaseDatabase],
) -> list[str]:
    """Comparing two lists of databases and return list of databases not existing in
    new databases list.

    Args:
        databases_old (list[dict]): _description_
        databases_new (list[dict]): _description_

    Returns:
        tuple: _description_
    """
    deleted_databases: list[str] = []
    existing_dbs = [database.name for database in databases_new]
    for database in databases_old:
        if database.name not in existing_dbs:
            deleted_databases.append(database.name)
            logger.info("Database %s deleted.", database.name)
    return deleted_databases


def compare_databases(
    repo_old: list[model_db.DatabaseDatabase], repo_new: list[model_db.DatabaseDatabase]
) -> tuple[list, dict]:
    """Comparing two repositories and returns name of deleted databases and schemas.

    Args:
        repo_new (dict): _description_
        repo_old (dict): _description_

    Returns:
        tuple: _description_
    """
    deleted_databases = find_deleted_databases(repo_old, repo_new)
    deleted_schemas_in_databases = {}
    existing_dbs = {database.name: database for database in repo_new}
    for database in repo_old:
        if database.name in deleted_databases:
            deleted_schemas_in_databases[
                database.name
            ] = find_deleted_schemas_in_databases(database)
        else:
            deleted_schemas_in_databases[
                database.name
            ] = find_deleted_schemas_in_databases(database, existing_dbs[database.name])
    return deleted_databases, deleted_schemas_in_databases
