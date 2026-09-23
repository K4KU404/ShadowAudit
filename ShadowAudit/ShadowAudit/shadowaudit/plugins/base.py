"""Contrato que todo plugin de auditoria precisa seguir."""

from abc import ABC, abstractmethod


class AuditPlugin(ABC):

    name = "Plugin"

    @abstractmethod
    def run(self, target: str) -> dict:
        """Executa o plugin contra um alvo autorizado e retorna o resultado."""
        raise NotImplementedError
