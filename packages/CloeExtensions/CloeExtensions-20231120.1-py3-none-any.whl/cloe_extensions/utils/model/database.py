from cloecore.utils.model.repository import database


class DatabaseTable(database.DatabaseTable):
    """Wrapper Class for DatabaseTable from CLOECore."""

    @staticmethod
    def _transform_string_bool(bool_string: str) -> bool:
        if bool_string.lower() == "yes":
            return True
        else:
            return False

    @staticmethod
    def _decide_datatype_precision(row, converter_params) -> str | None:
        data_type_precision = None
        if converter_params.datetime_precisions_column_name is not None:
            datetime_precisions = row[converter_params.datetime_precisions_column_name]
            if (
                datetime_precisions is None
                and converter_params.data_type_precisions_column_name is not None
            ):
                data_type_precision = row[
                    converter_params.data_type_precisions_column_name
                ]
            else:
                data_type_precision = datetime_precisions
        elif (
            converter_params.data_type_precisions_column_name is not None
            and converter_params.datetime_precisions_column_name is None
        ):
            data_type_precision = row[converter_params.data_type_precisions_column_name]
        return data_type_precision

    def add_columns(self, table_columns: list, converter_params) -> None:
        """
        Initialize TableColumn class for each column in the DatabaseTable and fill the
        TableColumns as a list of dictionaries.
        """
        for row in table_columns:
            data_type_length = None
            data_type_numeric_scale = None
            is_key = False
            is_nullable = False
            constraints = None
            column_name = row[converter_params.columns_column_name]
            ordinal_position = row[converter_params.ordinal_positions_column_name]
            data_type = row[converter_params.data_types_column_name]
            data_type_precision = self._decide_datatype_precision(row, converter_params)
            if converter_params.data_type_lengths_column_name is not None:
                data_type_length = row[converter_params.data_type_lengths_column_name]
            if converter_params.data_type_numeric_scales_column_name is not None:
                data_type_numeric_scale = row[
                    converter_params.data_type_numeric_scales_column_name
                ]
            if converter_params.is_key_column_name is not None:
                is_key = self._transform_string_bool(
                    row[converter_params.is_key_column_name]
                )
            if converter_params.is_nullable_column_name is not None:
                is_nullable = self._transform_string_bool(
                    row[converter_params.is_nullable_column_name]
                )
            if converter_params.constraints_column_name is not None:
                constraints = row[converter_params.constraints_column_name]
            tablecolumn = database.TableColumn(
                name=column_name,
                data_type=data_type,
                data_type_numeric_scale=data_type_numeric_scale,
                data_type_precision=data_type_precision,
                data_type_length=data_type_length,
                ordinal_position=ordinal_position,
                is_key=is_key,
                is_nullable=is_nullable,
                constraints=constraints,
            )
            self.columns.append(tablecolumn)
