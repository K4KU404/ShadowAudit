"""Executa os plugins de auditoria registrados, um por um."""

from shadowaudit.core.logger import get_logger

logger = get_logger(__name__)


class AuditRunner:
    """Orquestra a execucao dos plugins contra um alvo."""

    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        logger.debug("Registrando plugin: %s", plugin.name)
        self.plugins.append(plugin)

    def run(self, target: str) -> list:
        results = []
        logger.info("Iniciando auditoria em: %s", target)

        for plugin in self.plugins:
            logger.info("Executando plugin: %s", plugin.name)
            try:
                results.append(plugin.run(target))
            except Exception as exc:  # noqa: BLE001 - queremos capturar qualquer falha do plugin
                logger.error("Falha no plugin %s: %s", plugin.name, exc)
                results.append({
                    "plugin": plugin.name,
                    "target": target,
                    "status": "erro",
                    "error": str(exc),
                })

        logger.info("Auditoria finalizada. %d plugin(s) executado(s).", len(results))
        return results
