import logging
from typing import Any

import snowflake.connector
from snowflake.core import Root

from .connection_parameters import ConnectionParameters

logger = logging.getLogger(__name__)

snf_logger = logging.getLogger("snowflake")
snf_logger.setLevel(logging.WARNING)


class SnowflakeInterface:
    """
    Wraps Snowflake connector and adds
    functionality to it.
    """

    def __init__(self, connection_params: ConnectionParameters) -> None:
        self._snowflake_connection = snowflake.connector.connect(**connection_params.model_dump(exclude_none=True))

    def test_connection(self) -> None:
        """
        Tests the connection.
        """
        cur = self._snowflake_connection.cursor()
        try:
            cur.execute("SELECT current_version()")
            cur.fetchone()
        except Exception as error:
            logger.error("Connection could not be established.")
            raise error
        finally:
            cur.close()

    def get_root_object(self) -> Root:
        """
        Retrieve the root object initialized with the current Snowflake connection.

        This method creates and returns an instance of the `Root` class,
        initialized using the Snowflake connection associated with this instance.

        Returns:
            Root: An instance of the `Root` class initialized with the Snowflake connection.
        """
        root = Root(self._snowflake_connection)
        return root

    def get_connection_object(self) -> snowflake.connector.SnowflakeConnection:
        """
        Getter method to return the initialized snowflake connection.

        This methods returns an instance of snowflake.connector.SnowflakeConnection
        initialized using the Snowflake connection associated with this instance.

        Returns:
            snowflake.connector.SnowflakeConnection: Initialized Snowflake connection.
        """
        return self._snowflake_connection

    def run_one_with_return(self, query: str) -> list[dict[str, str]]:
        with self._snowflake_connection.cursor() as cur:
            try:
                cur.execute(query)
            except Exception as e:
                logger.error("There was an error executing the script.")
                raise e
            result = cur.fetchall()
            column_names = [row[0] for row in cur.description]
            result_w_names = [dict(zip(column_names, row)) for row in result]
        return result_w_names

    def _retrieve_query_queue(self, query_queue: list[str], continue_on_error: bool = True) -> None:
        """
        Retrieves status of all query ids in a queue list.
        """
        for sfqid in query_queue:
            try:
                if self._snowflake_connection.is_still_running(
                    self._snowflake_connection.get_query_status_throw_if_error(sfqid)
                ):
                    query_queue.append(sfqid)
            except snowflake.connector.ProgrammingError as error:
                logger.error("Programming Error after retrieval: %s", error)
                if not continue_on_error:
                    raise error

    def run_many(self, queries: list[str], continue_on_error: bool = True) -> None:
        """
        Execute multiple queries without return values.
        """
        query_queue: list[str] = []
        with self._snowflake_connection.cursor() as cur:
            for query in queries:
                try:
                    cur.execute_async(query)
                    if cur.sfqid:
                        query_queue.append(cur.sfqid)
                except snowflake.connector.ProgrammingError as error:
                    logger.error("Programming Error while executing: %s", error)
                    raise error
        self._retrieve_query_queue(query_queue, continue_on_error)

    def run_many_with_return(
        self, queries: dict[Any, str], continue_on_error: bool = True
    ) -> dict[Any, list[dict[str, str]] | None]:
        cur = self._snowflake_connection.cursor()
        query_queue = []
        query_results: dict[str, list[dict[str, str]] | None] = {}
        for q_id, query in queries.items():
            cur.execute_async(query)
            query_queue.append({"q_id": q_id, "sfqid": cur.sfqid})
        while query_queue:
            query_info = query_queue.pop(0)
            try:
                if self._snowflake_connection.is_still_running(
                    self._snowflake_connection.get_query_status_throw_if_error(query_info["sfqid"])
                ):
                    query_queue.append(query_info)
                else:
                    cur.get_results_from_sfqid(query_info["sfqid"])
                    result = cur.fetchall()
                    column_names = [row[0] for row in cur.description]
                    query_results[query_info["q_id"]] = [dict(zip(column_names, row)) for row in result]
            except snowflake.connector.ProgrammingError as e:
                logger.error("Programming Error: %s", e)
                if continue_on_error:
                    query_results[query_info["q_id"]] = None
                else:
                    raise e
        return query_results

    def close(self) -> None:
        self._snowflake_connection.close()
