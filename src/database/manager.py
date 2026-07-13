import sqlite3
from pathlib import Path


class DatabaseManager:
    """Handles the application's SQLite database."""

    def __init__(self):
        self.database_path = Path("data") / "cryptointel.db"
        self.connection = None

    def connect(self):
        """Connect to the SQLite database."""
        self.connection = sqlite3.connect(self.database_path)
        print("✓ Database connected")

    def create_tables(self):
        """Create all required database tables."""

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            website TEXT,
            discord TEXT,
            x TEXT,
            blockchain TEXT,
            category TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

        print("✓ Database tables verified")

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")


database = DatabaseManager()