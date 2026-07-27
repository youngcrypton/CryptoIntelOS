import sqlite3
from pathlib import Path


class DatabaseManager:
    """Handles SQLite database operations."""

    def __init__(self):
        self.database_path = Path("data") / "cryptointel.db"
        self.connection = None

    def connect(self):
        """Connect to the SQLite database."""

        self.connection = sqlite3.connect(self.database_path)

        print("✓ Database connected")

    def close(self):
        """Close the database connection."""

        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")

    def create_tables(self):
        """Create all required database tables."""

        cursor = self.connection.cursor()

        # ==========================
        # Projects
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                website TEXT,
                discord TEXT,
                x TEXT,
                blockchain TEXT,
                category TEXT,
                status TEXT DEFAULT 'Watching'
            )
            """
        )

        # ==========================
        # Events
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT NOT NULL,
                source TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                priority TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                evidence TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        # ==========================
        # Website Snapshots
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS website_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT NOT NULL,
                website TEXT NOT NULL,
                title TEXT,
                description TEXT,
                html_hash TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )

        # ==========================
        # X Profile Snapshots
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS x_profile_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT NOT NULL,
                username TEXT,
                display_name TEXT,
                bio TEXT,
                followers INTEGER,
                following INTEGER,
                verified INTEGER,
                website TEXT,
                joined TEXT,
                profile_image TEXT,
                banner_image TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

        print("✓ Database tables verified")


database = DatabaseManager()