from ..logging import LoggerMixin
from ..session import SessionManager


class TableManager(LoggerMixin):
    """TableManager class for managing tables in the catalog."""

    def __init__(self):
        self._spark = SessionManager.get_spark_session()
        self._utils = SessionManager.get_utils()
        self._console_logger = self.get_console_logger()
        self._console_logger.debug("TableManager initialized...")
        self._tabular_logger = self.get_tabular_logger(uc_table_name="TableManager")
        self._tabular_logger.debug("message:TableManager initialized.")

    @staticmethod
    def create_table():
        """Create a table in the catalog."""
        raise NotImplementedError

    def drop_table(self, table_identifier: str, delete_physical_data: bool = False):
        """Deletes a Table. For security reasons you are forced to pass the table_name.

        If delete_physical_data is True the actual physical data on the ADLS will be deleted.
        Use with caution!

        Args:
            table_identifier: The table identifier in the catalog. Must be in the format 'catalog.schema.table'.
            delete_physical_data: If set to True, deletes not only the metadata
                                  within the Catalog but also the physical data.
        """
        self._console_logger.info(f"Deleting table [ '{table_identifier}' ] ...")
        if not isinstance(table_identifier, str):
            raise NotImplementedError("table_identifier must be a string, can be a Table object in the future.")

        if delete_physical_data:
            self._delete_physical_data()
        self.drop_table_from_catalog(table_identifier)

    def drop_table_from_catalog(self, table_identifier: str) -> None:
        """Removes a table from the catalog. Physical data is retained.

        Args:
            table_identifier: The table identifier in the catalog. Must be in the format 'catalog.schema.table'.
        """
        self._console_logger.info(f"... deleting table [ '{table_identifier}' ] from Catalog.")
        if not isinstance(table_identifier, str):
            raise NotImplementedError("table_identifier must be a string, can be a Table object in the future.")
        self._spark.sql(f"DROP TABLE IF EXISTS {table_identifier};")

    def _delete_physical_data(self):
        """Removes the physical data on the ADLS for the location of this table.

        Raises:
            NotImplementedError: This can be implemented, once a Table object is available.
        """
        self._console_logger.info("... deleting physical data for table [ '' ] from Catalog.")
        raise NotImplementedError("This can be implemented, once a Table object is available.")
