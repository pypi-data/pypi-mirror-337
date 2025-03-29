import logging
import os
import re

import cloecore.utils.model.repository.database as model_db
from jinja2 import Environment

import cloe_extensions.snowflake_access_control.utils.compare_databases as c_db

logger = logging.getLogger(__name__)
MODEL_ENVIRONMENT = os.getenv("CLOE_MODEL_ENVIRONMENT", "DEV")
logger.debug(
    "Model environment initialized. Using '%s' as environment.", MODEL_ENVIRONMENT
)


class TechnicalRoles:
    """TechnicalRoles class filters database objects and integrates them
    into a fully working role concept.
    """

    def __init__(
        self,
        template_env: Environment,
        database_filter_positive: str | None = None,
        database_filter_negative: str | None = None,
    ) -> None:
        self.database_filter_positive = database_filter_positive
        self.database_filter_negative = database_filter_negative
        self.template_env = template_env
        self.templates = {
            "Database": {"DB OWNER": {"name": "role_db_owner.sql.j2", "group": "2"}},
            "Schema": {
                "SCHEMA OWNER": {"name": "role_ownership.sql.j2", "group": "2"},
                "READ": {"name": "role_read.sql.j2", "group": "2"},
                "WRITE": {"name": "role_write.sql.j2", "group": "2"},
                "EXECUTE": {"name": "role_execute.sql.j2", "group": "2"},
            },
        }
        self.deploy_groups = {
            role["group"]: ""
            for group in self.templates.values()
            for role in group.values()
        }
        self.deploy_groups["1"] = ""

    def filter_databases(
        self, databases: model_db.Databases
    ) -> list[model_db.DatabaseDatabase]:
        """Method filters all database entitites based on the specified
        regex pattern.

        Args:
            model_content (dict): cloe compatible database entities dict

        Returns:
            list: database entitties matching regex pattern
        """
        filtered_content = []
        for database in databases.model_content:
            if (
                not self.database_filter_positive
                or re.match(self.database_filter_positive, database.name)
            ) and (
                not self.database_filter_negative
                or not re.match(self.database_filter_negative, database.name)
            ):
                filtered_content.append(database)
        return filtered_content

    def deploy_groups_to_script(self) -> str:
        """Sorts deployment groups and concats group values
        based on sorting.

        Returns:
            str: _description_
        """
        all_queries = ""
        for group_name in sorted(self.deploy_groups):
            all_queries += f"-- CLOE TECHNICAL_ROLES -- GROUP {group_name}\n"
            all_queries += self.deploy_groups[group_name]
        return all_queries

    def create_roles(
        self,
        filtered_databases_new: list[model_db.DatabaseDatabase],
        filtered_databases_old: list[model_db.DatabaseDatabase] | None = None,
    ) -> None:
        """Method creates all necessary roles for a given set of database entities

        Args:
            filtered_repository (dict): cloe compatible database entities dict
        """
        databases_to_process, schemas_to_process = c_db.compare_databases(
            filtered_databases_new, filtered_databases_old
        )
        for database in filtered_databases_new:
            catalog_name = database.rendered_catalog_name
            schemas = [
                schema
                for schema in database.schemas
                if catalog_name in schemas_to_process
                and schema.name in schemas_to_process[catalog_name]
            ]
            if catalog_name in databases_to_process:
                logger.info(
                    "Creating role ddls %s for database %s",
                    list(self.templates["Database"].keys()),
                    catalog_name,
                )
                for role_name, role in self.templates["Database"].items():
                    logger.debug(
                        "Creating role ddl %s for database %s", role_name, catalog_name
                    )
                    self.deploy_groups["1"] += self.template_env.get_template(
                        role["name"]
                    ).render(database_name=catalog_name, create_role=True)
                    self.deploy_groups[role["group"]] += self.template_env.get_template(
                        role["name"]
                    ).render(database_name=catalog_name, grant_role=True)
            else:
                logger.info(
                    "Skipping role ddls %s for database %s",
                    list(self.templates["Database"].keys()),
                    catalog_name,
                )
            for schema in schemas:
                logger.info(
                    "Creating role ddls %s for schema %s in database %s",
                    list(self.templates["Schema"].keys()),
                    schema.name,
                    catalog_name,
                )
                for role_name, role in self.templates["Schema"].items():
                    logger.debug(
                        "Creating role ddl %s for schema %s in database %s",
                        role_name,
                        schema.name,
                        catalog_name,
                    )
                    self.deploy_groups["1"] += self.template_env.get_template(
                        role["name"]
                    ).render(
                        database_name=catalog_name,
                        schema_name=schema.name,
                        create_role=True,
                    )
                    self.deploy_groups[role["group"]] += self.template_env.get_template(
                        role["name"]
                    ).render(
                        database_name=catalog_name,
                        schema_name=schema.name,
                        grant_role=True,
                    )

    def delete_roles(
        self,
        filtered_databases_old: list[model_db.DatabaseDatabase],
        filtered_databases_new: list[model_db.DatabaseDatabase],
    ) -> None:
        """Method creates all drop roles for two sets of database entities.

        Args:
            filtered_repository_old (dict): _description_
            filtered_repository_new (dict): _description_
        """
        self.deploy_groups["0"] = ""
        deleted_databases, deleted_schemas = c_db.compare_databases(
            filtered_databases_old, filtered_databases_new
        )
        for catalog_name in deleted_databases:
            logger.warning(
                "Creating drop role dmls %s for database %s",
                list(self.templates["Database"].keys()),
                catalog_name,
            )
            for role in self.templates["Database"].values():
                logger.debug(
                    "Creating drop role dml %s for database %s",
                    role["name"],
                    catalog_name,
                )
                self.deploy_groups["0"] += self.template_env.get_template(
                    role["name"]
                ).render(database_name=catalog_name, delete_role=True)
        for catalog_name, schemas in deleted_schemas.items():
            for schema_name in schemas:
                logger.warning(
                    "Creating drop role dmls %s for schema %s in database %s",
                    list(self.templates["Schema"].keys()),
                    schema_name,
                    catalog_name,
                )
                for role in self.templates["Schema"].values():
                    logger.debug(
                        "Creating drop role dmls %s for schema %s in database %s",
                        role["name"],
                        schema_name,
                        catalog_name,
                    )
                    self.deploy_groups["0"] += self.template_env.get_template(
                        role["name"]
                    ).render(
                        database_name=catalog_name,
                        schema_name=schema_name,
                        delete_role=True,
                    )

    def generate_w_cleanup(
        self,
        databases: model_db.Databases,
        databases_old: model_db.Databases,
        create_roles_incremental: bool,
    ) -> str:
        """Wrapper function for generating role drops for deleted database objects.

        Args:
            repository_json (dict): _description_
            repository_old_json (dict): _description_

        Returns:
            str: _description_
        """
        filtered_repository_new = self.filter_databases(databases)
        filtered_repository_old = self.filter_databases(databases_old)
        if create_roles_incremental:
            self.create_roles(filtered_repository_new, filtered_repository_old)
        else:
            self.create_roles(filtered_repository_new)
        self.delete_roles(filtered_repository_old, filtered_repository_new)
        return self.deploy_groups_to_script()

    def generate_wo_cleanup(self, databases: model_db.Databases) -> str:
        """Method calling all methods for generating role conept based on json
        cloe metadata.

        Args:
            repository_json (dict): _description_

        Returns:
            str: _description_
        """
        repository = self.filter_databases(databases)
        self.create_roles(repository)
        return self.deploy_groups_to_script()
