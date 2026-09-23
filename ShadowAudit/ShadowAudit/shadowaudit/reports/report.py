"""Gera o relatorio JSON de uma auditoria."""

import json
import os
import re
from datetime import datetime, timezone


def _nome_arquivo_seguro(texto: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", texto)


def generate_json_report(target: str, results: list, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{_nome_arquivo_seguro(target)}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    report = {
        "target": target,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_plugins": len(results),
        "results": results,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return filepath
