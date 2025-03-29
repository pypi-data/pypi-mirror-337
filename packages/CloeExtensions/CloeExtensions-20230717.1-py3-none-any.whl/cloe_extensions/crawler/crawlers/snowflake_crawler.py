import logging
import re
import uuid

import cloecore.utils.model.repository.database as model_db
import jinja2 as j2
from cloecore.utils import model

from cloe_extensions.utils.db.snowflake import SnowflakeInterface

logger = logging.getLogger(__name__)


class SnowflakeCrawler:
    """Class to construct a crawler to retrieve snowflake metadata
    and transform to a CLOE compatible format.
    """

    def __init__(
        self,
        connection_uri_params: dict[str, str],
        ignore_columns: bool,
        ignore_tables: bool,
        templates_env: j2.Environment,
        database_filter: str | None = None,
        database_name_replace: str | None = None,
    ) -> None:
        self.snf_interface = SnowflakeInterface(connection_uri_params)
        self.databases: dict[str, model.DatabaseDatabase] = {}
        self.schemas: dict[str, list[model.DatabaseSchema]] = {}
        self.repository = model.Databases(model_content=[])
        self.ignore_columns: bool = ignore_columns
        self.ignore_tables: bool = ignore_tables
        self.templates_env: j2.Environment = templates_env
        self.database_filter = database_filter
        self.database_name_replace = database_name_replace

    def _get_databases(self) -> None:
        """Retrieves databases in snowflake and adds them to the repository."""
        query = "SHOW DATABASES"
        all_databases = self.snf_interface.run_one_with_return(query)
        result_w_names = []
        if self.database_filter is not None:
            pattern = re.compile(self.database_filter)
            for raw_database in all_databases:
                if pattern.match(raw_database["name"]) is not None:
                    result_w_names.append(raw_database)
        else:
            result_w_names = all_databases
        for row in result_w_names:
            db_name = row["name"]
            if db_name.lower() in ("snowflake", "snowflake_sample_data"):
                continue
            database = model.DatabaseDatabase(name=db_name, schemas=[])
            self.databases[database.name] = database
            self.repository.model_content.append(database)

    def _transform_table_columns(
        self, table_columns: list[dict[str, str]]
    ) -> dict[str, list[model_db.TableColumn]]:
        """Transforms a query result from a snowflake information schema
        columns view into a CLOE columns object and gathering all columns
        of all table in a dict.

        Args:
            table_columns (list): _description_

        Returns:
            dict: _description_
        """
        tables: dict[str, list[model_db.TableColumn]] = {}
        for row in table_columns:
            if f"{row['TABLE_SCHEMA']}{row['TABLE_NAME']}" not in tables:
                tables[f"{row['TABLE_SCHEMA']}{row['TABLE_NAME']}"] = []
            column = model_db.TableColumn(
                name=row["COLUMN_NAME"],
                ordinal_position=row["ORDINAL_POSITION"],
                is_key=row["IS_IDENTITY"],
                is_nullable=row["IS_NULLABLE"],
                data_type=row["DATA_TYPE"],
                constraints=row["COLUMN_DEFAULT"],
                data_type_length=row["CHARACTER_MAXIMUM_LENGTH"],
                data_type_numeric_scale=row["NUMERIC_SCALE"],
                data_type_precision=row["NUMERIC_PRECISION"],
            )
            tables[f"{row['TABLE_SCHEMA']}{row['TABLE_NAME']}"].append(column)
        return tables

    def _get_schemas(self) -> None:
        """Retrieves schemas in snowflake and saves them in the
        corrspeonding database"""
        queries = {}
        for database in self.repository.model_content:
            queries[database.name] = self.templates_env.get_template(
                "schema_retrieve.sql.j2"
            ).render(database_name=database.name)
        logger.debug("Queries for schema crawl created.")
        result_w_names = self.snf_interface.run_many_with_return(queries)
        logger.debug("Schema crawl results retrieved.")
        for database_name, result in result_w_names.items():
            if not result:
                continue
            for row in result:
                schema = model.DatabaseSchema(name=row["SCHEMA_NAME"])
                self.databases[database_name].schemas.append(schema)
                if database_name not in self.schemas:
                    self.schemas[database_name] = []
                self.schemas[database_name].append(schema)

    def _get_tables(self) -> None:
        """Retrieves tables in snowflake and saves them in the corrspeonding schema"""
        queries = {}
        for database in self.repository.model_content:
            if not self.ignore_columns:
                queries[database.name] = self.templates_env.get_template(
                    "column_retrieve.sql.j2"
                ).render(database_name=database.name)
            else:
                queries[database.name] = self.templates_env.get_template(
                    "table_retrieve.sql.j2"
                ).render(database_name=database.name)
        logger.debug("Queries for tables crawl created.")
        result_w_names = self.snf_interface.run_many_with_return(queries)
        logger.debug("Tables crawl results retrieved.")
        for database_name, result in result_w_names.items():
            if result is None:
                continue
            schemas: dict[str, list[model.DatabaseTable]] = {
                schema_name: []
                for schema_name in sorted(set([row["TABLE_SCHEMA"] for row in result]))
            }
            table_columns = {}
            if not self.ignore_columns:
                table_columns = self._transform_table_columns(result)
            for table_info in sorted(
                set([(row["TABLE_SCHEMA"], row["TABLE_NAME"]) for row in result]),
                key=lambda x: "".join(x),
            ):
                new_table = model.DatabaseTable(
                    id=uuid.uuid4(),
                    name=table_info[1],
                    schema_name=table_info[0],
                    columns=table_columns.get(f"{table_info[0]}{table_info[1]}", []),
                )
                schemas[table_info[0]].append(new_table)
            for schema_name, schema_tables in schemas.items():
                schema = model.DatabaseSchema(name=schema_name, tables=schema_tables)
                self.databases[database_name].schemas.append(schema)

    def _transform(self) -> None:
        """Transform databases in a CLOE json format."""
        for database in self.repository.model_content:
            if self.database_name_replace is not None:
                database.name = re.sub(
                    self.database_name_replace,
                    r"{{ CLOE_BUILD_CRAWLER_DB_REPLACEMENT }}",
                    database.name,
                )

    def to_json(self) -> str:
        return self.repository.json(indent=4, by_alias=True, exclude_none=True)

    def crawl(self) -> None:
        """Crawls a snowflake instance and saves metadata
        in a CLOE compatible format
        """
        self._get_databases()
        if self.ignore_tables:
            self._get_schemas()
        else:
            self._get_tables()
        self._transform()
        self.snf_interface.close()
