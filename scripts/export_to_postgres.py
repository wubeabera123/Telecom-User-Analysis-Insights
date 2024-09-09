import psycopg2
import pandas as pd

class UserSatisfactionExporterPostgres:
    def __init__(self, db_config):
        # Initialize with database connection details
        self.db_config = db_config
        self.connection = None

    def connect_to_db(self):
        """Establishes a connection to the PostgreSQL database."""
        self.connection = psycopg2.connect(
            host=self.db_config['localhost'],
            port=self.db_config['5432'],
            user=self.db_config['postgres'],
            password=self.db_config['12345'],
            database=self.db_config['telecom_db']
        )
    
    def export_to_postgres(self, data):
        """Exports the DataFrame to PostgreSQL."""
        cursor = self.connection.cursor()

        # Create a table to hold the data if it doesn't already exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_satisfaction_scores (
            id SERIAL PRIMARY KEY,
            imsi VARCHAR(50),
            engagement_score FLOAT,
            experience_score FLOAT,
            satisfaction_score FLOAT
        );
        """
        cursor.execute(create_table_query)

        # Insert DataFrame rows into the table
        for _, row in data.iterrows():
            insert_query = """
            INSERT INTO user_satisfaction_scores (imsi, engagement_score, experience_score, satisfaction_score)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                str(row['IMSI']),
                float(row['Engagement Score']),
                float(row['Experience Score']),
                float(row['Satisfaction Score'])
            ))

        # Commit the transaction
        self.connection.commit()
        cursor.close()

    def fetch_exported_data(self):
        """Fetches the inserted data from PostgreSQL for verification."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_satisfaction_scores LIMIT 10;")
        result = cursor.fetchall()
        cursor.close()
        return result

    def close_connection(self):
        """Closes the PostgreSQL database connection."""
        if self.connection:
            self.connection.close()

