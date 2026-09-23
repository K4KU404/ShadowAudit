"""Persistencia dos resultados de auditoria em SQLite."""

import json
import os
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target TEXT NOT NULL,
    plugin TEXT NOT NULL,
    status TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class Database:

    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(SCHEMA)

    def save_results(self, target: str, results: list) -> None:
        agora = datetime.now(timezone.utc).isoformat()

        with self._connect() as conn:
            for result in results:
                conn.execute(
                    "INSERT INTO audits (target, plugin, status, result_json, created_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        target,
                        result.get("plugin", "desconhecido"),
                        result.get("status", "desconhecido"),
                        json.dumps(result, ensure_ascii=False),
                        agora,
                    ),
                )

    def fetch_all(self) -> list:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM audits ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]
