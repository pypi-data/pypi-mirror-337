from jinja2 import Environment, Template


class WarehouseGrant:
    """Represents a warehouse grant to functional role."""

    def __init__(
        self,
        name: str,
        template: Template,
        usage: bool | None = None,
        operate: bool | None = None,
    ) -> None:
        self.name = name
        self.usage = usage
        self.operate = operate
        self.template = template

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.usage is True:
            self.usage = False
        if self.operate is True:
            self.operate = False

    def gen_sql(self, role_name: str) -> str:
        """Generates SQL snippets for
        wh privileges.

        Returns:
            str: _description_
        """
        return self.template.render(
            usage=self.usage,
            operate=self.operate,
            warehouse_name=self.name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )


class SchemaGrant:
    """Represents a schema grant to functional role."""

    def __init__(
        self,
        name: str,
        template: Template,
        read: bool | None = None,
        write: bool | None = None,
        execute: bool | None = None,
        owner: bool | None = None,
    ) -> None:
        self.name = name
        self.read = read
        self.write = write
        self.execute = execute
        self.owner = owner
        self.template = template

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.read is True:
            self.read = False
        if self.write is True:
            self.write = False
        if self.execute is True:
            self.execute = False
        if self.owner is True:
            self.owner = False

    def gen_sql(self, database_name: str, role_name: str) -> str:
        """Generates SQL snippets for
        schema privileges.

        Returns:
            str: _description_
        """
        return self.template.render(
            read=self.read,
            write=self.write,
            execute=self.execute,
            owner=self.owner,
            schema_name=self.name,
            database_name=database_name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )


class DatabaseGrant:
    """Represents a database grant to functional role."""

    def __init__(
        self,
        name: str,
        template_db: Template,
        template_schema: Template,
        owner: bool | None = None,
        schemas: list | None = None,
    ) -> None:
        self.name = name
        self.owner = owner
        self.schemas = []
        self.template = template_db
        if schemas:
            self.schemas = [
                SchemaGrant(template=template_schema, **schema) for schema in schemas
            ]

    def remove_grants(self) -> None:
        """Removes all set grants."""
        if self.owner is True:
            self.owner = False
        for schema in self.schemas:
            schema.remove_grants()

    def _gen_sql(self, role_name: str) -> str:
        """Generates SQL snippets for
        database privileges.

        Returns:
            str: _description_
        """
        return self.template.render(
            owner=self.owner,
            database_name=self.name,
            role_name=role_name,
            use_doublequotes_for_name=True,
        )

    def gen_sql(self, role_name: str) -> str:
        """Combines all snippets and queries and
        returns them.

        Args:
            role_name (str): _description_

        Returns:
            str: _description_
        """
        queries = self._gen_sql(role_name)
        for schema in self.schemas:
            queries += schema.gen_sql(self.name, role_name)
        return queries


class FunctionalRole:
    """Represents a functional role in snowflake."""

    def __init__(
        self,
        name: str,
        template_env: Environment,
        warehouses: list | None = None,
        databases: list | None = None,
        additional_grants: list | None = None,
    ) -> None:
        self.name = name
        self.template_env = template_env
        self.warehouses = []
        self.databases = []
        self.additional_grants = []
        self.deploy_groups = {"1": "", "2": "", "3": ""}
        if warehouses:
            wh_template = template_env.get_template("set_warehouse_privileges.sql.j2")
            self.warehouses = [
                WarehouseGrant(template=wh_template, **wh) for wh in warehouses
            ]
        if databases:
            db_template = template_env.get_template("set_database_privileges.sql.j2")
            schema_template = template_env.get_template("set_schema_privileges.sql.j2")
            self.databases = [
                DatabaseGrant(
                    template_db=db_template, template_schema=schema_template, **db
                )
                for db in databases
            ]
        if additional_grants:
            self.additional_grants = additional_grants
        self.deleted = False

    def set_deleted(self) -> None:
        """Set role to deleted state."""
        self.deleted = True

    def deploy_groups_to_script(self) -> str:
        """Sorts deployment groups and concats group values
        based on sorting.

        Returns:
            str: _description_
        """
        all_queries = ""
        for group_name in sorted(self.deploy_groups):
            all_queries += f"-- CLOE FUNCTIONAL_ROLES -- GROUP {group_name}\n"
            all_queries += self.deploy_groups[group_name]
        return all_queries

    def gen_sql(self) -> None:
        """Combines all snippets and queries and
        returns them.

        Args:
            role_name (str): _description_
        """
        use_doublequotes_for_name = True
        name = f'"{self.name}"' if use_doublequotes_for_name is True else self.name
        if self.deleted:
            self.deploy_groups["1"] = f"DROP ROLE IF EXISTS {name};\n"
        else:
            self.deploy_groups["1"] = f"CREATE ROLE IF NOT EXISTS {name};\n"
            self.deploy_groups["2"] = f"GRANT ROLE {name} TO ROLE SYSADMIN;\n"
            for warehouse in self.warehouses:
                self.deploy_groups["2"] += warehouse.gen_sql(self.name)
            for database in self.databases:
                self.deploy_groups["2"] += database.gen_sql(self.name)
            self.deploy_groups["3"] += "\n".join(self.additional_grants)

    def create_sql_script(self) -> str:
        """Combines a list of queries and returns
        a script.

        Returns:
            str: _description_
        """
        self.gen_sql()
        return self.deploy_groups_to_script()
