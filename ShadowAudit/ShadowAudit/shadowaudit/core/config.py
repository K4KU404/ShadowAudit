"""Le config.yaml e expoe as configuracoes do projeto."""

import os
from dataclasses import dataclass, field

try:
    import yaml
except ImportError:
    yaml = None

CONFIG_PATH = "config.yaml"

PADRAO = {
    "database": {"path": "database/shadowaudit.db"},
    "reports": {"output_dir": "reports_output"},
    "plugins": {"enabled": ["ExamplePlugin"]},
}


@dataclass
class Config:
    database_path: str = PADRAO["database"]["path"]
    reports_dir: str = PADRAO["reports"]["output_dir"]
    enabled_plugins: list = field(default_factory=lambda: list(PADRAO["plugins"]["enabled"]))

    @classmethod
    def load(cls, path: str = CONFIG_PATH) -> "Config":
        data = PADRAO

        if yaml is not None and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                carregado = yaml.safe_load(f) or {}
            data = {**PADRAO, **carregado}

        return cls(
            database_path=data.get("database", {}).get("path", PADRAO["database"]["path"]),
            reports_dir=data.get("reports", {}).get("output_dir", PADRAO["reports"]["output_dir"]),
            enabled_plugins=data.get("plugins", {}).get("enabled", PADRAO["plugins"]["enabled"]),
        )
