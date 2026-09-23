"""Ponto de entrada do ShadowAudit. Execute com: python -m shadowaudit.main"""

from shadowaudit.cli import parse_args
from shadowaudit.core.banner import print_banner
from shadowaudit.core.config import Config
from shadowaudit.core.display import clear_screen, print_results
from shadowaudit.core.logger import get_logger
from shadowaudit.core.runner import AuditRunner
from shadowaudit.database.db import Database
from shadowaudit.plugins.example import ExamplePlugin
from shadowaudit.plugins.http_headers import HTTPHeadersPlugin
from shadowaudit.plugins.port_scanner import PortScannerPlugin
from shadowaudit.plugins.ssl_cert import SSLCertPlugin
from shadowaudit.reports.report import generate_json_report

logger = get_logger(__name__)

# Plugins disponiveis, referenciados pelo nome usado em config.yaml
AVAILABLE_PLUGINS = {
    "ExamplePlugin": ExamplePlugin,
    "HTTPHeadersPlugin": HTTPHeadersPlugin,
    "PortScannerPlugin": PortScannerPlugin,
    "SSLCertPlugin": SSLCertPlugin,
}

COMANDOS_SAIDA = ("sair", "exit", "q", "quit")


def build_runner(enabled_plugins: list) -> AuditRunner:
    runner = AuditRunner()
    for plugin_name in enabled_plugins:
        plugin_class = AVAILABLE_PLUGINS.get(plugin_name)
        if plugin_class is None:
            logger.warning("Plugin desconhecido no config: %s", plugin_name)
            continue
        runner.register_plugin(plugin_class())
    return runner


def run_audit(target: str, args, config: Config) -> None:
    """Roda a auditoria completa contra um alvo e trata db/relatorio."""
    if not args.yes:
        confirmacao = input(
            f'Voce confirma que tem autorizacao para auditar "{target}"? (s/n): '
        ).strip().lower()
        if confirmacao != "s":
            logger.info("Execucao cancelada pelo usuario.")
            return

    runner = build_runner(config.enabled_plugins)
    results = runner.run(target)

    print_results(target, results)

    if not args.no_db:
        db = Database(config.database_path)
        db.save_results(target, results)
        logger.info("Resultados salvos em %s", config.database_path)

    if not args.no_report:
        filepath = generate_json_report(target, results, config.reports_dir)
        logger.info("Relatorio gerado em %s", filepath)


def main():
    args = parse_args()
    config = Config.load(args.config)

    # Modo direto: --target foi passado (uso em scripts/CI), roda uma vez e sai
    if args.target:
        if not args.no_banner:
            print_banner()
        run_audit(args.target, args, config)
        return

    # Modo interativo: fica em loop, limpando a tela a cada nova auditoria
    while True:
        clear_screen()
        if not args.no_banner:
            print_banner()

        target = input("Digite o alvo autorizado (ou 'sair' para encerrar): ").strip()

        if target.lower() in COMANDOS_SAIDA:
            print("\nAte mais!")
            break

        if not target:
            input("Nenhum alvo informado. Pressione ENTER para tentar novamente...")
            continue

        run_audit(target, args, config)
        input("\nPressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    main()
