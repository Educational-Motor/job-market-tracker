from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

# Returns a psycopg2 connection using credentials from the .env file.
# Import this wherever you need a database connection instead of repeating the connection logic.
def get_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "prefer")
    )
    return connection


if __name__ == "__main__":
    conn = get_connection()
    print("Connected successfully")
    conn.close()
