"""Testes da camada de persistencia (Database). Rodar com: pytest"""

import os

from shadowaudit.database.db import Database


def test_save_and_fetch_results(tmp_path):
    db_path = os.path.join(tmp_path, "test.db")
    db = Database(db_path)

    results = [{"plugin": "Example Plugin", "target": "alvo.local", "status": "executado"}]
    db.save_results("alvo.local", results)
    saved = db.fetch_all()

    assert len(saved) == 1
    assert saved[0]["target"] == "alvo.local"
    assert saved[0]["status"] == "executado"
