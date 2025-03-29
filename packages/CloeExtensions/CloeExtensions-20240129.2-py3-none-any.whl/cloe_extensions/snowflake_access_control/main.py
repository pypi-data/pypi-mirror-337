import logging
import pathlib

import cloecore.utils.exceptions as custom_errors
from cloecore.utils import reader, writer
from jinja2 import Environment, PackageLoader

import cloe_extensions.utils.reader as extreader
from cloe_extensions.snowflake_access_control.snowflake import (
    FunctionalRole,
    RoleDeployer,
    TechnicalRoles,
)
from cloe_extensions.snowflake_access_control.utils import compare_func_model
from cloe_extensions.snowflake_access_control.utils.json_utils import (
    read_model_from_json,
)
from cloe_extensions.utils.gitclient import GitClient

logger = logging.getLogger(__name__)
TEMPLATE_ENV = Environment(
    loader=PackageLoader("cloe_extensions.snowflake_access_control", "templates")
)


def generate_technical_roles(
    git_root_path: pathlib.Path,
    output_path: pathlib.Path,
    database_model_filepath: pathlib.Path,
    database_model_previous_filepath: pathlib.Path | None = None,
    git_tag_regex: str | None = None,
    database_filter_positive: str | None = None,
    database_filter_negative: str | None = None,
    use_incremental_mode: bool = False,
) -> None:
    """Main entrypoint function to generate roles

    Args:
        git_root_path (str): _description_
        output_path (str): _description_
        database_model_filepath (str): _description_
        database_model_previous_filepath (str | None, optional): _description_.
        Defaults to None.
        git_tag_regex (str | None, optional): _description_. Defaults to None.
        database_filter_positive (str | None, optional): _description_.
        Defaults to None.
        database_filter_negative (str | None, optional): _description_.
        Defaults to None.
        use_incremental_mode (bool, optional): _description_.
        Defaults to False.

    Raises:
        SystemExit: _description_
    """
    if use_incremental_mode and git_tag_regex is None:
        raise ValueError(
            "If use_incremental_mode is used, a git_tag_regex has to be supplied!"
        )
    files_found = reader.read_models_from_disk(
        [git_root_path / database_model_filepath]
    )
    errors = custom_errors.SupportError()
    databases = reader.read_database_file(errors, files_found)
    errors.log_report()
    tech_roles = TechnicalRoles(
        template_env=TEMPLATE_ENV,
        database_filter_positive=database_filter_positive,
        database_filter_negative=database_filter_negative,
    )
    if git_tag_regex is None:
        tech_roles_script = tech_roles.generate_wo_cleanup(databases)
    else:
        git_client = GitClient(git_root_path, git_tag_regex)
        databases_old = reader.read_database_file(
            errors,
            read_model_from_json(
                git_client.get_json_from_tag(
                    database_model_previous_filepath or database_model_filepath
                )
            ),
        )
        tech_roles_script = tech_roles.generate_w_cleanup(
            databases,
            databases_old,
            use_incremental_mode,
        )
    writer.write_string_to_disk(tech_roles_script, output_path / "tech_roles.sql")


def generate_functional_roles(
    git_root_path: pathlib.Path,
    output_path: pathlib.Path,
    func_model_filepath: pathlib.Path,
    func_model_previous_filepath: pathlib.Path | None = None,
    git_tag_regex: str | None = None,
) -> None:
    """Main entrypoint function to generate functional roles.

    Args:
        git_root_path (str): _description_
        output_path (str): _description_
        func_model_filepath (str): _description_
        func_model_previous_filepath (str | None, optional): _description_.
        Defaults to None.
        git_tag_regex (str | None, optional): _description_. Defaults to None.
    """
    func_model = (
        extreader.read_yaml_from_disk(git_root_path / func_model_filepath) or {}
    )
    func_roles = [
        FunctionalRole(name=name, template_env=TEMPLATE_ENV, **attributes)
        for name, attributes in func_model.items()
    ]
    if git_tag_regex is not None:
        git_client = GitClient(git_root_path, git_tag_regex)
        func_model_old = (
            git_client.get_yaml_from_tag(
                func_model_previous_filepath or func_model_filepath
            )
            or {}
        )
        func_roles_old = [
            FunctionalRole(name=name, template_env=TEMPLATE_ENV, **attributes)
            for name, attributes in func_model_old.items()
        ]
        func_roles = compare_func_model(func_roles_old, func_roles)
    scripts = [role.create_sql_script() for role in func_roles]
    writer.write_string_to_disk("\n".join(scripts), output_path / "func_roles.sql")


def deploy(
    input_sql_path: pathlib.Path,
    snowflake_conn_params: dict[str, str],
    continue_on_error: bool = True,
) -> None:
    """main entrypoint function to deploy roles

    Args:
        input_sql_path (str): _description_
        snowflake_conn_params (dict): _description_. Defaults to None.
    """
    role_deployer = RoleDeployer(connection_uri_params=snowflake_conn_params)
    sql_script = extreader.read_text_from_disk(input_sql_path)
    role_deployer.role_deploy(sql_script, continue_on_error)
