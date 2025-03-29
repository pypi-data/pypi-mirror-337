import logging
import re

from cloe_extensions.utils.db import snowflake

logger = logging.getLogger(__name__)


class RoleDeployer(snowflake.SnowflakeInterface):
    """Wrapper class for Snowflake interface. Adding functionality
    for role deployment.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.deploy_groups: dict[str, str] = {}

    def create_deploy_groups(self, sql_script: str) -> None:
        """Extracts headers from sql script and groups queries into
        deployment groups

        Args:
            sql_script (str): _description_
        """
        if "TECHNICAL_ROLES" in sql_script:
            splits = sql_script.split("-- CLOE TECHNICAL_ROLES -- ")
        elif "FUNCTIONAL_ROLES" in sql_script:
            splits = sql_script.split("-- CLOE FUNCTIONAL_ROLES -- ")
        else:
            logger.error("Malformed header or unknown role script type.")
        for split in splits:
            if len(split) < 1:
                continue
            header = split.splitlines()[0]
            if match := re.search(r"GROUP\s+(\d+)", header, re.IGNORECASE):
                group = match.group(1)
            else:
                logger.error(
                    "Malformed SQL script CLOE header. Manual changes made to script?"
                )
                raise SystemExit("Malformed SQL script CLOE header.")
            if group not in self.deploy_groups:
                self.deploy_groups[group] = ""
            self.deploy_groups[group] += split.split("\n", maxsplit=1)[1]

    def role_deploy(self, sql_script: str, continue_on_error: bool = True) -> None:
        """Method for deploying roles in an asynchronous way."""
        self.create_deploy_groups(sql_script)
        for group in sorted(self.deploy_groups):
            sql_group_split = [
                query
                for query in self.deploy_groups[group].split(";")
                if len(query) > 1
            ]
            logger.info("Starting deployment of group: %s", group)
            self.run_many(sql_group_split, continue_on_error=continue_on_error)
