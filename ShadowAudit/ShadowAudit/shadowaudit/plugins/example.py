"""Plugin de exemplo, usado como referencia para criar novos plugins."""

from datetime import datetime, timezone

from shadowaudit.plugins.base import AuditPlugin


class ExamplePlugin(AuditPlugin):

    name = "Example Plugin"

    def run(self, target: str) -> dict:
        return {
            "plugin": self.name,
            "target": target,
            "status": "executado",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
