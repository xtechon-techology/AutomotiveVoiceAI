import pyodbc
import pandas as pd
import logging
from decimal import Decimal


from connectors.data_connector import DataConnector

logger = logging.getLogger(__name__)


class SQLServerDatabaseConnector(DataConnector):
    """
    A connector for managing SQL Server Database connections and executing queries.
    Extends the base class DataConnector.
    """

    def __init__(self ):
        super().__init__()
        self.connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:voicepocsqlserver.database.windows.net,1433;Database=voicepocdb;Uid=voicepoc;Pwd=Officenoida@24dec;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    def establish_connection(self):
        """
        Establish a connection to the SQL Server database.
        """
        try:
            self.session = pyodbc.connect(self.connection_string)
            logger.info("Successfully connected to SQL Server.")
        except Exception as e:
            logger.error("Failed to connect to SQL Server.", exc_info=True)
            raise RuntimeError("Failed to establish connection.")

    def execute_query_with_summary(self, query):
        """
        Execute a query and fetch the results along with a summary.
        """
        try:
            self.establish_connection()
            with self.session.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    return "No data found.", [], {}

                column_names = [col[0] for col in cursor.description]
                result_dict = {col: [] for col in column_names}

                for row in rows:
                    for idx, val in enumerate(row):
                        result_dict[column_names[idx]].append(
                            self._convert_decimal_to_float(val)
                        )

                df = pd.DataFrame(result_dict)
                summary = df.describe()
                return summary, column_names, result_dict, df
        except Exception as e:
            logger.error("Error executing query.", exc_info=True)
            raise RuntimeError(e)
        finally:
            self.terminate_session()

    def validate_sql(self, query):
        """
        Validate a SQL query by executing it.
        """
        try:
            self.establish_connection()
            with self.session.cursor() as cursor:
                cursor.execute(query)
                return True, ""
        except Exception as e:
            logger.error(f"Query validation error: {e}", exc_info=True)
            return False, str(e)
        finally:
            self.terminate_session()

    def fetch_column_metadata(self, table_name):
        """
        Fetch column names and data types for a given table.
        """
        try:
            schema, table = table_name.split(".")
            query = (
                f"SELECT COLUMN_NAME, DATA_TYPE "
                f"FROM INFORMATION_SCHEMA.COLUMNS "
                f"WHERE TABLE_NAME='{table}' AND TABLE_SCHEMA='{schema}'"
            )
            _, column_names, results = self.execute_query_with_summary(query)
            return [{"column_name": row[0], "data_type": row[1]} for row in results]
        except Exception as e:
            logger.error("Error fetching column metadata.", exc_info=True)
            raise RuntimeError(e)

    def _convert_decimal_to_float(self, data):
        """
        Convert Decimal to float for JSON serialization.
        """
        return float(data) if isinstance(data, Decimal) else data


# Example usage
def main():
    connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:voicepocsqlserver.database.windows.net,1433;Database=voicepocdb;Uid=voicepoc;Pwd=Officenoida@24dec;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    connector = SQLServerDatabaseConnector()

    query = "SELECT TOP 10 * FROM ServiceJobs;"
    summary, column_names, results, df = connector.execute_query_with_summary(query)

    print(summary)
    print(column_names)
    print(results)


if __name__ == "__main__":
    main()
