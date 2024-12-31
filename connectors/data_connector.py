import pyodbc
import pandas as pd
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class DataConnector:
    """
    A base class for managing connections and executing operations.
    This class is intended to be extended by specific data processors.
    """

    VALIDATION_RETRY_LIMIT = 3

    def __init__(self):
        """Initialize the connector with a placeholder for the connection object."""
        self.session = None
        self.connection_string = None

    def establish_connection(self):
        """
        Establish a connection to the data source or service.
        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "The 'establish_connection' method must be implemented by the subclass."
        )

    def execute_operation(self, operation, **kwargs):
        """
        Execute an operation using the established session.

        Parameters:
            operation (str): The operation or command to be executed.
            **kwargs: Additional parameters for the operation execution.

        Raises:
            RuntimeError: If the session is not established.
        """
        if self.session is None:
            raise RuntimeError(
                "Session has not been established. Please establish a connection first."
            )
        pass

    def fetch_results(self, operation, **kwargs):
        """
        Execute an operation and fetch results using the established session.

        Parameters:
            operation (str): The operation or command to be executed.
            **kwargs: Additional parameters for fetching results.

        Raises:
            RuntimeError: If the session is not established.
        """
        if self.session is None:
            raise RuntimeError(
                "Session has not been established. Please establish a connection first."
            )
        pass

    def terminate_session(self):
        """
        Terminate the session.
        """
        try:
            if self.session is not None:
                self.session.close()
                self.session = None
        except Exception as e:
            logger.error(f"Error while terminating the session: {e}", exc_info=True)
            raise RuntimeError(f"Error while terminating the session: {e}")
