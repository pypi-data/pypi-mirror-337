import logging
from typing import Any

import pyodbc

logger = logging.getLogger(__name__)


class MSSQLInterface:
    """Wraps Snowflake connector and adds
    functionality to it.
    """

    def __init__(self, connection_uri_params: dict[str, str]) -> None:
        self.connection = pyodbc.connect(
            (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={connection_uri_params['SERVER']};"
                f"DATABASE={connection_uri_params['DATABASE']};"
                f"UID={connection_uri_params['UID']};PWD={connection_uri_params['PWD']}"
            ),
            autocommit=True,
        )

    def test_connections(self) -> None:
        """Tests the connection.

        Raises:
            e: _description_
        """
        cur = self.connection.cursor()
        try:
            cur.execute("SELECT 1")
            cur.fetchone()
        except Exception as error:
            logger.error("Connection could not be established.")
            raise error
        finally:
            cur.close()

    def run_one_with_return(self, query: str) -> list[dict[str, str]]:
        with self.connection.cursor() as cur:
            try:
                cur.execute(query)
            except Exception as e:
                logger.error("There was an error executing the script.")
                raise e
            result = cur.fetchall()
            column_names = [row[0] for row in cur.description]
            result_w_names = [dict(zip(column_names, row)) for row in result]
        return result_w_names

    def run_many(self, queries: list[str]) -> None:
        """Execute multiple queries without return values.

        Args:
            queries (list[str]): _description_
            continue_on_error (bool, optional): _description_. Defaults to True.

        Raises:
            error: _description_
        """
        with self.connection.cursor() as cur:
            for query in queries:
                try:
                    cur.execute(query)
                except pyodbc.ProgrammingError as error:
                    logger.error("Programming Error while executing: %s", error)
                    raise error

    def run_many_with_return(
        self, queries: dict[Any, str], continue_on_error: bool = True
    ) -> dict[Any, list[dict[str, str]] | None]:
        cur = self.connection.cursor()
        query_results: dict[str, list[dict[str, str]] | None] = {}
        with self.connection.cursor() as cur:
            for q_id, query in queries.items():
                try:
                    cur.execute(query)
                    result = cur.fetchall()
                    column_names = [row[0] for row in cur.description]
                    query_results[q_id] = [
                        dict(zip(column_names, row)) for row in result
                    ]
                except pyodbc.ProgrammingError as error:
                    logger.error("Programming Error while executing: %s", error)
                    if continue_on_error:
                        query_results[q_id] = None
        return query_results

    def close(self) -> None:
        self.connection.close()
