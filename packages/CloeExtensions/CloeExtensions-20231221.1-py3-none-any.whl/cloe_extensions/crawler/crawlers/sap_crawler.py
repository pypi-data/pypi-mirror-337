import uuid

import cloecore.utils.model.repository.database as model_db
from cloecore.utils import model

try:
    from pyrfc import Connection

    dependency_available = True
except ImportError:
    Connection = None
    dependency_available = False


class SapCrawler:
    def __init__(
        self,
        connection_uri_params: dict[str, str],
        sap_object_type: str,
        sap_tables: list[str] | None = None,
        sap_odp_context: str = "",
        sap_odp_objects: list[str] | None = None,
    ) -> None:
        self.ashost = connection_uri_params["host"]
        self.sap_client = connection_uri_params["client"]
        self.sysnr = connection_uri_params["sysno"]
        self.sap_object_type = sap_object_type
        self.sap_tables = sap_tables or []
        self.sap_odp_context = sap_odp_context
        self.sap_odp_objects = sap_odp_objects or []

        if not dependency_available:
            raise ImportError("pyrfc is required for this feature.")

        self.conn = Connection(
            ashost=self.ashost,
            sysnr=self.sysnr,
            client=self.sap_client,
            user=connection_uri_params["user"],
            passwd=connection_uri_params["password"],
        )

    def _get_table_metadata(
        self, table: str, MaxRows: int = 1000, FromRow: int = 0
    ) -> list[model_db.TableColumn]:
        """Query metadata of an SAP table with RFC_READ_TABLE"""

        # Choose data dictionary fields to return
        input_fields: list[str] = [
            "TABNAME",
            "FIELDNAME",
            "POSITION",
            "KEYFLAG",
            "INTTYPE",
            "INTLEN",
            "NOTNULL",
            "DATATYPE",
            "LENG",
            "DECIMALS",
        ]
        input_fields_formatted = [{"FIELDNAME": x} for x in input_fields]

        # where statement
        options = [{"TEXT": "TABNAME = '" + table + "'"}]

        # rfc
        table_information_tables: dict = self.conn.call(
            "RFC_READ_TABLE",
            QUERY_TABLE="DD03L",
            DELIMITER="|",
            FIELDS=input_fields_formatted,
            OPTIONS=options,
            ROWCOUNT=MaxRows,
            ROWSKIPS=FromRow,
        )

        # split fields and fields_name to hold the data and the column names
        fields: list[str] = []
        data_fields = table_information_tables["DATA"]

        # parse data fields into a list
        for line in range(0, len(data_fields)):
            fields.append(data_fields[line]["WA"].strip())

        rows: list[list[str]] = [row.split("|") for row in fields]

        table_columns: list[model_db.TableColumn] = []
        for row in rows:
            row = [elem.strip() for elem in row]
            column = model_db.TableColumn(
                name=row[1],
                ordinal_position=int(row[2]),
                is_key=True if row[3] == "X" else False,
                is_nullable=True if row[6] == "X" else False,
                data_type=row[7],
                data_type_numeric_scale=int(row[9]),
                data_type_precision=int(row[8]),
            )
            table_columns.append(column)

        return table_columns

    def _get_odp_metadata(
        self, odpContext: str, odpObject: str
    ) -> list[model_db.TableColumn]:
        """Query metadata of an SAP ODP object with RODPS_REPL_ODP_GET_DETAIL"""

        # rfc
        tables = self.conn.call(
            "RODPS_REPL_ODP_GET_DETAIL",
            I_SUBSCRIBER_TYPE="BOBJ_DS",
            I_CONTEXT=odpContext,
            I_ODPNAME=odpObject,
        )

        supportsFull = tables["E_SUPPORTS_FULL"]
        supportsFull = 1 if supportsFull == "X" else 0

        supportsDelta = tables["E_SUPPORTS_DELTA"]
        supportsDelta = 1 if supportsDelta == "X" else 0

        et_fields = tables["ET_FIELDS"]
        table_columns: list[model_db.TableColumn] = []
        for row in et_fields:
            column = model_db.TableColumn(
                name=row["NAME"],
                is_key=True if row["KEYFLAG"] == "X" else False,
                is_nullable=not row["KEYFLAG"],
                data_type_length=int(row["OUTPUTLENG"]),
                data_type=row["TYPE"],
                data_type_numeric_scale=int(row["DECIMALS"]),
                data_type_precision=int(row["LENGTH"]),
                comment=(
                    f'{row["DESCRIPTION"]} - SupportsFull: {supportsFull}'
                    f" - SupportsDelta: {supportsDelta}"
                ),
            )
            table_columns.append(column)

        return table_columns

    def table_crawl(self) -> list[model.DatabaseTable]:
        all_tables = []
        for table_name in self.sap_tables:
            table_columns = self._get_table_metadata(table_name)
            new_table = model.DatabaseTable(
                id=uuid.uuid4(),
                name=table_name,
                schema_name=self.sap_client,
                columns=table_columns,
            )
            all_tables.append(new_table)
        return all_tables

    def odp_crawl(self) -> list[model.DatabaseTable]:
        all_tables = []
        for odp_object in self.sap_odp_objects:
            table_columns = self._get_odp_metadata(self.sap_odp_context, odp_object)
            new_table = model.DatabaseTable(
                id=uuid.uuid4(),
                name=odp_object,
                level="src",
                schema_name=self.sap_client,
                columns=table_columns,
            )
            all_tables.append(new_table)
        return all_tables

    def crawl(self) -> None:
        if self.sap_object_type == "table":
            all_tables = self.table_crawl()
        elif self.sap_object_type == "odp":
            all_tables = self.odp_crawl()
        schema = model.DatabaseSchema(name=self.sap_object_type, tables=all_tables)
        database = model.DatabaseDatabase(
            name=f"{self.ashost}{self.sysnr}{self.sap_client}", schemas=[schema]
        )
        self.repository = model.Databases(model_content=[database])
