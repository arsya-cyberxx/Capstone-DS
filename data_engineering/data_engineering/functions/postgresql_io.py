"""This module does connect & run query in postgresql using sqlalchemy."""
import os

import pandas as pd
from sqlalchemy import create_engine, text

class PGStorageHandler:
    """
    Class to handle all table handling purposes, related to Postgresql.
    """
    def __init__(self):
        self.engine = self.create_postgres_engine()

    def create_postgres_engine(self):
        """
        Creates a SQLAlchemy engine object for connecting to PostgreSQL.

        : return : sqlalchemy.engine.Engine: A SQLAlchemy engine object.
        """
        username = os.environ["_PG_USERNAME"]
        password = os.environ["_PG_PASSWORD"]
        hostname = os.environ["_PG_HOSTNAME"]
        port = os.environ["_PG_PORT"]
        database = os.environ["_PG_DATABASE"]
        connection_string = f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
        engine = create_engine(
            connection_string,
            connect_args={"options": "-c search_path=public,staging"}
        )
        return engine

    def execute_query(self, query):
        """
        Executes an SQL query using SQLAlchemy.

        :param query: SQL query as a string
        :return: Query results (if SELECT) or execution success message
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))

                # If it's a SELECT query, return fetched data
                if query.strip().lower().startswith("select"):
                    return pd.DataFrame(result.fetchall())
                else:
                    return "Query executed successfully."
        except Exception as e:
            return f"Error executing query: {e}"

    def df_to_table(self, df, table_name):
        """
        Loads a Pandas DataFrame into a PostgreSQL table using SQLAlchemy.

        :param df: Pandas DataFrame
        :param table_name: Target table name in PostgreSQL
        """
        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"Data successfully loaded into '{table_name}' table.")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
