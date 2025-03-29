import logging
from typing import Dict, List, Union

import snowflake.connector
from policy_tool.utils.logger_utils import LoggingAdapter, LogOperation, LogStatus

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)

class SnowClientConfig(object):
    def __init__(
        self,
        account: str,
        user: str,
        password: str,
        warehouse: str = None,
        role: str = None,
        database: str = None,
        sql_variables: dict = None,
    ):
        self.user = user
        self.password = password
        self.account = account
        self.warehouse = warehouse
        self.role = role
        self.database = database
        self.sql_variables = {} if sql_variables is None else sql_variables

    def get_connect_info(self) -> Dict:
        connect_info = {
            "account": self.account,
            "user": self.user,
            "password": self.password,
        }
        for opt_prop in ["warehouse", "role", "database"]:
            if getattr(self, opt_prop) is not None:
                connect_info[opt_prop] = getattr(self, opt_prop)

        return connect_info
class SnowClient(object):
    """
    Objects that collects all operations and information about the snowflake databases.
    """

    def __init__(self, snowflake_configuration: SnowClientConfig):
        """
            Creates a new SnowClient
        Args:
            config: SolutionConfig - stored configuration values
        """
        self.connection = None
        self._config = snowflake_configuration
        self.database = snowflake_configuration.database

    def __del__(self):
        """
        Ensures the connection snowflake is closed at the end
        """
        if self.connection is not None:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.connection is not None:
            self.connection.close()

    def _get_connection(self):
        """
        Factory method to get snowflake connection
        Initializes new snowflake connection if not already connected
        """
        if self.connection is None:
            conn_info = self._config.get_connect_info()
            self.connection = snowflake.connector.connect(**conn_info)

            if self._config.database is not None:
                self.execute_statement(f"USE DATABASE {self.database};")

            self.set_sql_variables(self._config.sql_variables)

        return self.connection

    @staticmethod
    def _get_error_message(excepction: Exception, statement: str) -> None:
        """
        Compose error message if the execution of a statement or query fails.
        """
        if hasattr(excepction, "raw_msg"):
            message = excepction.raw_msg.replace("\n", " ")
        else:
            message = str(
                excepction
            )  # this makes sure that all kinds of errors can have a message, even if they do not have raw_msg attribute
        if hasattr(excepction, "sfqid"):
            message = message + f"\nQuery ID: {excepction.sfqid}"
        return f"SNOWFLAKE ERROR: {message}\nFailed statement:\n{statement}"

    def execute_statement(self, statement: Union[str, List[str]]) -> None:
        """
            Executes simple statement against snowflake
            Schema and Database settings must be set beforehand
        Args:
            statement Union[str, List[str]] - a sql statement or a list of sql statements to execute
        """
        connection = self._get_connection()
        statement_list: List[str] = (
            statement if isinstance(statement, list) else [statement]
        )

        try:
            for single_statement in statement_list:
                stripped_statement = (
                    single_statement.strip()
                )  # remove whitespace from statement, as execute_string() might produce warnings if empty new lines are found after a semicolon
                log.debug(
                    f"START execution [ '{stripped_statement}' ]",
                    operation=LogOperation.SQLCOMMAND,
                    status=LogStatus.PENDING,
                    db=self.database,
                )
                _ = connection.execute_string(stripped_statement)
                log.debug(
                    f"FINISH execution [ '{stripped_statement}' ]",
                    operation=LogOperation.SQLCOMMAND,
                    status=LogStatus.SUCCESS,
                    db=self.database,
                )

        except Exception as err:
            raise Exception(self._get_error_message(err, single_statement)) from err

    def execute_query(
        self, query: Union[str, List[str]], use_dict_cursor: bool = True
    ) -> Union[List[Dict], List[List[Dict]]]:
        """
            Executes sql statements and against snowflake and returns the result as dictionary or list of dictionaries
        Args:
            query Union[str, List[str]] - a sql query or a list of sql queries to execute
            use_dict_cursor bool (default true) - use snowflake DictCursor for results instead of returning a list
        """
        connection = self._get_connection()
        if use_dict_cursor is True:
            cursor = connection.cursor(snowflake.connector.DictCursor)
        else:
            cursor = connection.cursor()

        query_list: List[str] = query if isinstance(query, list) else [query]
        result: List[Dict] = []

        try:
            for single_query in query_list:
                log.debug(
                    f"START execution [ '{single_query}' ]",
                    operation=LogOperation.SQLCOMMAND,
                    status=LogStatus.PENDING,
                    db=self.database,
                )
                result.append(cursor.execute(single_query).fetchall())
                log.debug(
                    f"FINISH execution [ '{single_query}' ]",
                    operation=LogOperation.SQLCOMMAND,
                    status=LogStatus.SUCCESS,
                    db=self.database,
                )
        except Exception as err:
            raise Exception(self._get_error_message(err, single_query)) from err

        return result[0] if not isinstance(query, list) else result

    def set_sql_variables(self, variables_dict: dict) -> None:
        """
            Set given SQL variables for the session

            Supported variable types: int, float, bool, str
        Args
            variables_dict: dict - dictionary containing the variables to be set, example: {"varname1": "varvalue1", "varname2": "varvalue2"}
        """
        log.debug("SET sql variables")
        for key, value in variables_dict.items():
            if isinstance(value, int):
                value_string = str(value)
            elif isinstance(value, float):
                value_string = str(value)
            elif isinstance(value, bool):
                if value:
                    value_string = "TRUE"
                else:
                    value_string = "FALSE"
            else:
                if "'" in value:
                    raise ValueError(
                        f"Variable [ '{key}' ] contains illegal character \"'\"."
                    )
                value_string = f"'{value}'"
            statement = f"SET {key} = {value_string}"
            self.execute_statement(statement)

    @staticmethod
    def split_snowflake_list_representation(list_representation: str) -> list:

        if not list_representation:
            return []

        if list_representation.startswith("[") and list_representation.endswith("]"):
            list_representation = list_representation[1:-1]

        if list_representation == "":
            return []

        list_representation = list_representation.replace('"','').strip()

        l = [entry.strip() for entry in list_representation.split(",")]

        return l
