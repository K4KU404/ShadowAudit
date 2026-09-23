"""Testes do AuditRunner e do ExamplePlugin. Rodar com: pytest"""

from shadowaudit.core.runner import AuditRunner
from shadowaudit.plugins.example import ExamplePlugin


def test_runner_executa_plugin_registrado():
    runner = AuditRunner()
    runner.register_plugin(ExamplePlugin())

    results = runner.run("alvo.teste.local")

    assert len(results) == 1
    assert results[0]["plugin"] == "Example Plugin"
    assert results[0]["status"] == "executado"


def test_runner_sem_plugins_retorna_lista_vazia():
    runner = AuditRunner()
    assert runner.run("alvo.teste.local") == []


class PluginComErro:
    name = "Plugin Quebrado"

    def run(self, target):
        raise ValueError("falha proposital")


def test_runner_captura_erro_de_plugin():
    runner = AuditRunner()
    runner.register_plugin(PluginComErro())

    results = runner.run("alvo.teste.local")

    assert results[0]["status"] == "erro"
    assert "falha proposital" in results[0]["error"]
