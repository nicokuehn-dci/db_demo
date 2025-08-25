import psycopg2
import os

load_dotenv()

connection_string = f"""
    host={os.getenv("DB_HOST")}
    dbname={os.getenv("DB_NAME")}
    user={os.getenv("DB_USER")}
    password={os.getenv("DB_PASSWORD")}
    port={os.getenv("DB_PORT")}
"""
