import pathlib
from typing import Literal

import click

import cloe_extensions.crawler as crawl


@click.command()
@click.argument(
    "output_json_path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "--sap-user",
    envvar="CLOE_SAP_USER",
    required=True,
    help="The SAP user the crawler should use. If not set is expected as CLOE_SAP_USER env variable.",
)
@click.option(
    "--sap-password",
    envvar="CLOE_SAP_PASSWORD",
    required=True,
    help="The SAP password the crawler should use. If not set is expected as CLOE_SAP_PASSWORD env variable.",
)
@click.option(
    "--sap-client",
    envvar="CLOE_SAP_CLIENT",
    required=True,
    help="The SAP client the crawler should use. If not set is expected as CLOE_SAP_CLIENT env variable.",
)
@click.option(
    "--sap-sysno",
    envvar="CLOE_SAP_SYSNO",
    required=True,
    help="The SAP system number the crawler should use. If not set is expected as CLOE_SAP_SYSNO env variable.",
)
@click.option(
    "--sap-host",
    envvar="CLOE_SAP_HOST",
    required=True,
    help="The SAP host / server IP the crawler should use. If not set is expected as CLOE_SAP_HOST env variable.",
)
@click.option(
    "--sap-object-type",
    required=True,
    help="TABLE or ODP. If not set is expected as CLOE_SAP_OBJECT_TYPE.",
)
@click.option(
    "--sap-tables",
    required=False,
    multiple=True,
    help="The SAP tables that should be extracted by the crawler. If not set is expected as CLOE_SAP_TABLES env variable.",
)
@click.option(
    "--sap-odp-context",
    required=False,
    help="ODP context: SAPI, BW, HANA, ABAP_CDS (If object typ is odp). If not set is expected as CLOE_SAP_ODP_CONTEXT.",
)
@click.option(
    "--sap-odp-objects",
    required=False,
    multiple=True,
    help="The SAP ODP objects that should be extracted by the crawler. If not set is expected as CLOE_SAP_ODP_OBJECTS env variable.",
)
@click.option(
    "--existing-model-path",
    required=False,
    type=click.Path(
        exists=True, resolve_path=True, writable=True, path_type=pathlib.Path
    ),
    help="Reference an existing Repository json to update.",
)
def crawl_sap(
    output_json_path: pathlib.Path,
    sap_user: str,
    sap_password: str,
    sap_client: str,
    sap_sysno: str,
    sap_host: str,
    sap_object_type: Literal["table", "odp"],
    sap_tables: list[str],
    sap_odp_context: str,
    sap_odp_objects: list[str],
    existing_model_path: pathlib.Path | None = None,
) -> None:
    """This script extracts the metadata from a SAP Netweaver system
    and returns the information in a CLOE compatible json format."""
    sap_conn_params = {
        "user": sap_user,
        "password": sap_password,
        "client": sap_client,
        "sysno": sap_sysno,
        "host": sap_host,
    }

    crawl.crawl(
        output_json_path,
        sap_conn_params,
        True,
        True,
        "sap",
        existing_model_path=existing_model_path,
        sap_object_type=sap_object_type,
        sap_tables=sap_tables,
        sap_odp_context=sap_odp_context,
        sap_odp_objects=sap_odp_objects,
    )
