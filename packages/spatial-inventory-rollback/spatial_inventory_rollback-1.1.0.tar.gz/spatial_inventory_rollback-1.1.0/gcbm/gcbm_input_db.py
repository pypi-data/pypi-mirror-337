import os
import pandas as pd
import sqlite3


def read_query(query_name: str) -> str:
    """Reads and returns the contents of:
    <this module path>/query/{queryname}.sql

    Args:
        query_name (str): name of the query to read

    Returns:
        str: contents of the query file
    """
    query_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "query",
        f"{query_name}.sql",
    )
    with open(query_path) as query_file:
        return query_file.read()


class GCBMInputDB:
    """Methods for reading the GCBM formatted sqlite database

    Args:
        path (str): path to a sqlite formatted GCBM input database
    """

    def __init__(self, path):
        self.path = path

    def query(self, query_name: str, params=None) -> pd.DataFrame:
        """runs a stored read query in this package directory
        (see dir: "./query") and returns the result as a pandas.DataFrame

        For example::

            running:

            query("stand_replacing_disturbance_matrix")

            will:

                1. open and read the file:
                    "./query/stand_replacing_disturbance_matrix.sql"
                2. query the connection in this instance into a
                    pandas.DataFrame. (see the function: pandas.read_sql)
                3. return the DataFrame

        Args:
            query_name (str): name of a file without extension in the "./query"
                dir
            params (list, tuple or dict, optional): The sql parameters to pass
                to the query. Defaults to None.

        Returns:
            pandas.DataFrame: the query result as a pandas.DataFrame
        """
        with sqlite3.connect(self.path) as connection:
            return pd.read_sql(
                sql=read_query(query_name), con=connection, params=params
            )
