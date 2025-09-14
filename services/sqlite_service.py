import sqlite3
import logging
import os
from datetime import datetime
from typing import Optional
from models import ApiKey
import secrets
import string

logger = logging.getLogger(__name__)


class SqliteService:
    """Service class for SQLite database operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the SQLite service
        
        Args:
            db_path: Path to the SQLite database file. If None, uses SQLITE_PATH env var or default 'data.sqlite'
        """
        if db_path is None:
            self.db_path = os.getenv('SQLITE_PATH', 'data.sqlite')
        else:
            self.db_path = db_path
            
        logger.info(f"Initializing SQLite service with database path: {self.db_path}")
        self._initialize_database()
    
    def _initialize_database(self):
        """
        Initialize the database and create the log-urls table if it doesn't exist
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create log-urls table if it doesn't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "log-urls" (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        title TEXT NOT NULL,
                        url TEXT NOT NULL
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "api-keys" (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        key TEXT NOT NULL,
                        username TEXT NOT NULL
                    )
                ''')

                conn.commit()
                logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def log_url_conversion(self, title: str, url: str, timestamp: Optional[str] = None):
        """
        Log a URL conversion to the database
        
        Args:
            title: The filename/title of the generated file
            url: The URL that was converted
            timestamp: Optional timestamp. If not provided, uses current time
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO "log-urls" (timestamp, title, url)
                    VALUES (?, ?, ?)
                ''', (timestamp, title, url))
                
                conn.commit()
                logger.debug(f"Logged URL conversion: {url} -> {title} at {timestamp}")
                
        except sqlite3.Error as e:
            logger.error(f"Error logging URL conversion: {e}")
            raise


    def get_database_info(self):
        """
        Get basic information about the database
        
        Returns:
            Dictionary with database information
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total count of logged URLs
                cursor.execute('SELECT COUNT(*) FROM "log-urls"')
                total_logs = cursor.fetchone()[0]
                
                # Get database file size
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    'database_path': self.db_path,
                    'total_logged_urls': total_logs,
                    'database_size_bytes': db_size,
                    'database_exists': os.path.exists(self.db_path)
                }
                
        except sqlite3.Error as e:
            logger.error(f"Error getting database info: {e}")
            raise

    def find_api_key_by_username(self, username: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    select *
                    from "api-keys"
                    where 1 = 1
                        and username = ?
                ''', [username])
                res = cursor.fetchone()
                key = ApiKey(*res) if res else None
                return key
        except sqlite3.Error as e:
            logger.error(f"Error generating new api key: {e}")
            raise

    def find_api_key_by_key(self, key: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    select *
                    from "api-keys"
                    where 1 = 1
                        and key = ?
                ''', [key])
                res = cursor.fetchone()
                key = ApiKey(*res) if res else None
                return key
        except sqlite3.Error as e:
            logger.error(f"Error generating new api key: {e}")
            raise

    def create_new_api_key(self, username: str):
        old_key = self.find_api_key_by_username(username)
        if old_key:
            raise Exception(f'username {username} already exists')
        alphabet = string.ascii_letters + string.digits
        secret = "".join(secrets.choice(alphabet) for  _ in range(32))
        new_key = ApiKey(id=None, timestamp=datetime.now(), key=secret, username=username)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    insert into "api-keys" (
                        timestamp,
                        key,
                        username
                    ) values (?, ?, ?)
                ''', (new_key.timestamp, new_key.key, new_key.username))

                conn.commit()

                return new_key
        except sqlite3.Error as e:
            logger.error(f"Error generating new api key: {e}")
            raise
