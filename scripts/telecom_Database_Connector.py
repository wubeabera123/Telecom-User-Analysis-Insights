import psycopg2
import pandas as pd

class TelecomDatabaseConnector:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        """
        Initialize the class with connection details to PostgreSQL.
        """
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def query_data(self, query):
        """
        Executes a SQL query and returns the result as a DataFrame.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            # Fetch all data
            data = cursor.fetchall()
            # Get column names
            column_names = [desc[0] for desc in cursor.description]
            # Return data as DataFrame
            return pd.DataFrame(data, columns=column_names)

    def close_connection(self):
        """
        Closes the database connection.
        """
        self.connection.close()
