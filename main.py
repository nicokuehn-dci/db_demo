import sqlite3
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define SQLite database file
DB_FILE = os.path.join(os.path.dirname(__file__), "local_db.sqlite")

# Print that we're trying to connect
print(f"Attempting to connect to SQLite database at: {DB_FILE}")

# For posterity - keep the PostgreSQL connection string in case we switch back later
# connection_string = f"""
#     host={os.getenv("DB_HOST")}
#     dbname={os.getenv("DB_NAME")}
#     user={os.getenv("DB_USER")}
#     password={os.getenv("DB_PASSWORD")}
#     port={os.getenv("DB_PORT")}
# """


def get_connection():
    """Establish a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f'Connected to SQLite database at {DB_FILE}!')
        return conn
    except Exception as e:
        print(f'Connection failed: {e}')
        return None


def create_tables(conn):
    """Create tables in SQLite database."""
    if not conn:
        print("No connection available")
        return False
        
    try:
        # Create a cursor
        cur = conn.cursor()
        
        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create posts table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        print("Tables created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False


def insert_sample_data(conn):
    """Insert sample data into tables."""
    if not conn:
        print("No connection available")
        return False
        
    try:
        # Create a cursor
        cur = conn.cursor()
        
        # Insert sample users
        cur.execute("DELETE FROM users")  # Clear existing data
        users = [
            ('user1', 'user1@example.com'),
            ('user2', 'user2@example.com')
        ]
        
        for user in users:
            cur.execute('''
                INSERT INTO users (username, email)
                VALUES (?, ?)
            ''', user)
            
        # Insert sample posts
        cur.execute("DELETE FROM posts")  # Clear existing data
        
        # Get user IDs
        cur.execute("SELECT id FROM users WHERE username='user1'")
        user1_id = cur.fetchone()[0]
        
        cur.execute("SELECT id FROM users WHERE username='user2'")
        user2_id = cur.fetchone()[0]
        
        posts = [
            (user1_id, 'First Post', 'This is the content of the first post.'),
            (user1_id, 'Second Post', 'This is the content of the second post.'),
            (user2_id, 'Hello World', 'Hello world from user2!')
        ]
        
        for post in posts:
            cur.execute('''
                INSERT INTO posts (user_id, title, content)
                VALUES (?, ?, ?)
            ''', post)
            
        conn.commit()
        print("Sample data inserted successfully!")
        return True
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        conn.rollback()
        return False


def run_sample_queries(conn):
    """Run sample queries to test our database setup."""
    if not conn:
        print("No connection available")
        return False
        
    try:
        # Create a cursor
        cur = conn.cursor()
        
        # Get users
        print("\n--- USERS ---")
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        for user in users:
            print(f"User ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
            
        # Get posts with author names
        print("\n--- POSTS ---")
        cur.execute("""
            SELECT p.id, u.username, p.title, p.content 
            FROM posts p 
            JOIN users u ON p.user_id = u.id
            ORDER BY p.id
        """)
        posts = cur.fetchall()
        for post in posts:
            print(f"Post ID: {post[0]}")
            print(f"Author: {post[1]}")
            print(f"Title: {post[2]}")
            print(f"Content: {post[3]}")
            print("-" * 40)
            
        cur.close()
        return True
        
    except Exception as e:
        print(f"Error running queries: {e}")
        return False


# Main execution
conn = get_connection()
if conn:
    if create_tables(conn):
        if insert_sample_data(conn):
            run_sample_queries(conn)
    conn.close()
    print("\nDatabase connection closed.")
else:
    print("Could not establish database connection.")
