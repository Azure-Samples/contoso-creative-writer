import pyodbc
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_to_database() -> pyodbc.Connection:
    """Connect to the Azure SQL Database."""
    try:
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DATABASE')
        username = os.getenv('AZURE_SQL_USERNAME')
        password = os.getenv('AZURE_SQL_PASSWORD')
        driver = '{ODBC Driver 17 for SQL Server}'

        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)
        logging.info(f"Connected to the Azure SQL Database at {server}")
        return conn
    except pyodbc.Error as e:
        logging.error(f"Error connecting to the Azure SQL Database: {e}")
        return None

def close_database_connection(conn: pyodbc.Connection) -> None:
    """Close the database connection."""
    try:
        if conn:
            conn.close()
            logging.info("Database connection closed.")
    except pyodbc.Error as e:
        logging.error(f"Error closing the database connection: {e}")

# Example usage with context management
class DatabaseConnection:
    def __enter__(self) -> pyodbc.Connection:
        self.conn = connect_to_database()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        close_database_connection(self.conn)

# Example usage
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        if conn:
            # Perform database operations
            pass
