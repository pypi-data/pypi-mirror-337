import sqlite3
import os
from pathlib import Path


class Database:
    def __init__(self):
        self.db_path = os.path.join(Path.home(), ".ta", "config.db")
        self._ensure_db_dir()
        self._init_db()

    def _ensure_db_dir(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """
            )
            conn.commit()

    def get_config(self, key: str) -> str:
        """获取配置值"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None

    def set_config(self, key: str, value: str):
        """设置配置值"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO config (key, value)
                VALUES (?, ?)
            """,
                (key, value),
            )
            conn.commit()
