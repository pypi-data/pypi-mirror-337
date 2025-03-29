import click

import cloe_extensions.crawler.cli as crawl_cli


@click.group()
def crawler_cli():
    """Endpoint to register new CLI commands.
    should be used by all extension CLIs having
    a crawler like purpose.
    """
    pass


crawler_cli.add_command(crawl_cli.crawl_snowflake)
crawler_cli.add_command(crawl_cli.crawl_mssql)
crawler_cli.add_command(crawl_cli.crawl_sap)
